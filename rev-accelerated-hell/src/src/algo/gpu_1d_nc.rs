use std::ffi::CString;
use rustacuda::{prelude::*, launch};
use crate::math::*;
use crate::algo::fft_algo::FftAlgorithm;
use crate::params::Params;

const BLOCKSIZE: u32 = 64;

pub struct GPUFFT1DNC {
    n: usize,
    modulus: i64,
    forward_phi: DeviceBuffer<i64>,
    reverse_phi: DeviceBuffer<i64>,
    forward_table: DeviceBuffer<i64>,
    reverse_table: DeviceBuffer<i64>,
    inverse_n: i64,
    module: Module,
    stream: Stream
}

impl GPUFFT1DNC {

    fn compute_tables(n: usize, root: i64, modulus: i64) -> (DeviceBuffer<i64>, DeviceBuffer<i64>){
        let mut forward_table = vec![1; n];
        let mut reverse_table = vec![1; n];
        let mut w = 1;
        for i in 0..n {
            forward_table[i] = w;
            if i != 0 {
                reverse_table[n-i] = w;
            }
            w = root * w % modulus;
        }
        return (DeviceBuffer::from_slice(&forward_table).unwrap(), DeviceBuffer::from_slice(&reverse_table).unwrap())
    }

    fn compute_phi(n: usize, root: i64, modulus: i64) -> (DeviceBuffer<i64>, DeviceBuffer<i64>) {
        let mut forward_phi = vec![1; n];
        let mut reverse_phi = vec![1; n];
        let mut w = 1;
        for i in 0..n {
            forward_phi[i] = w;
            w = root * w % modulus;
        }
        w = root * w % modulus;
        for i in 0..n {
            reverse_phi[n-1-i] = w;
            w = root * w % modulus;
        }
        return (DeviceBuffer::from_slice(&forward_phi).unwrap(), DeviceBuffer::from_slice(&reverse_phi).unwrap())
    }

    // A lighter-weight code version of NTT that leaves things in GPU format for further processing.
    fn gpuntt(&mut self, values: &mut DeviceBuffer<i64>, reverse: bool) -> DeviceBuffer<i64> {
        let mut resbuf: DeviceBuffer<i64> = unsafe { DeviceBuffer::uninitialized(self.n).unwrap() };
        let table = if reverse { &mut self.reverse_table } else { &mut self.forward_table };
        let grid_dim = (self.n as u32 + BLOCKSIZE - 1) / BLOCKSIZE;
        let func_name = CString::new("a").unwrap();
        let f = self.module.get_function(&func_name).unwrap();
        let stream = &self.stream;

        unsafe {
            launch!(f<<<grid_dim, BLOCKSIZE, 0, stream>>>(
                values.as_device_ptr(),
                table.as_device_ptr(),
                resbuf.as_device_ptr(),
                self.n as u32,
                self.modulus
            )).unwrap();
        }
        // Remember to synchronize and copy at caller
        resbuf
    }
}

impl FftAlgorithm for GPUFFT1DNC {
    type Polynomial = DeviceBuffer<i64>;

    fn new(params: Params) -> Self {
        // precompute powers of roots for FFT
        let (forward_table, reverse_table) = GPUFFT1DNC::compute_tables(params.degree, params.root * params.root % params.modulus, params.modulus);

        // precompute powers of phi for negacyclic
        let (forward_phi, reverse_phi) = GPUFFT1DNC::compute_phi(params.degree, params.root, params.modulus);

        let ptx = CString::new(include_str!("../../ptx/mystery")).unwrap();
        let module = Module::load_from_string(&ptx).unwrap();
        let stream = Stream::new(StreamFlags::NON_BLOCKING, None).unwrap();

        GPUFFT1DNC {
            n: params.degree,
            modulus: params.modulus,
            forward_phi,
            reverse_phi,
            forward_table,
            reverse_table,
            inverse_n: inverse(params.degree as i64, params.modulus),
            module,
            stream
        }
    }

    fn from_coeffs(&mut self, mut v: Vec<i64>) -> Self::Polynomial {
        v.resize(self.n, 0);
        let mut vbuf = DeviceBuffer::from_slice(&v).unwrap();
        let grid_dim = (self.n as u32 + BLOCKSIZE - 1) / BLOCKSIZE;
        let func_name = CString::new("d").unwrap();
        let f = self.module.get_function(&func_name).unwrap();
        let stream = &self.stream;

        unsafe {
            launch!(f<<<grid_dim, BLOCKSIZE, 0, stream>>>(
                vbuf.as_device_ptr(),
                self.forward_phi.as_device_ptr(),
                self.n as u32,
                1 as i64,
                self.modulus
            )).unwrap();
        }

        let res = self.gpuntt(&mut vbuf, false);
        res
    }

    fn to_coeffs(&mut self, mut poly: Self::Polynomial) -> Vec<i64> {
        let mut res = self.gpuntt(&mut poly, true);
        
        let grid_dim = (self.n as u32 + BLOCKSIZE - 1) / BLOCKSIZE;
        let func_name = CString::new("d").unwrap();
        let f = self.module.get_function(&func_name).unwrap();
        let stream = &self.stream;

        unsafe {
            launch!(f<<<grid_dim, BLOCKSIZE, 0, stream>>>(
                res.as_device_ptr(),
                self.reverse_phi.as_device_ptr(),
                self.n as u32,
                self.inverse_n,
                self.modulus
            )).unwrap();
        }
        let mut v = vec![0; self.n];
        stream.synchronize().unwrap();
        res.copy_to(&mut v).unwrap();
        v
    }

    fn add(&mut self, mut p1: Self::Polynomial, mut p2: Self::Polynomial) -> Self::Polynomial {
        // point-wise addition
        let grid_dim = (self.n as u32 + BLOCKSIZE - 1) / BLOCKSIZE;
        let func_name = CString::new("b").unwrap();
        let f = self.module.get_function(&func_name).unwrap();
        let stream = &self.stream;

        unsafe {
            launch!(f<<<grid_dim, BLOCKSIZE, 0, stream>>>(
                p1.as_device_ptr(),
                p2.as_device_ptr(),
                self.n as u32,
                self.modulus
            )).unwrap();
        }
        p1
    }
    fn mul(&mut self, mut p1: Self::Polynomial, mut p2: Self::Polynomial) -> Self::Polynomial {
        // point-wise multiplication
        let grid_dim = (self.n as u32 + BLOCKSIZE - 1) / BLOCKSIZE;
        let func_name = CString::new("c").unwrap();
        let f = self.module.get_function(&func_name).unwrap();
        let stream = &self.stream;

        unsafe {
            launch!(f<<<grid_dim, BLOCKSIZE, 0, stream>>>(
                p1.as_device_ptr(),
                p2.as_device_ptr(),
                self.n as u32,
                self.modulus
            )).unwrap();
        }
        // no reduction needed (thanks NC)
        p1
    }
}
