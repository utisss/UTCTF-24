extern "C" __global__ void a(const int64_t* vals, const int64_t* table, int64_t* result, uint n, int64_t modulus) {
    uint i = blockIdx.x * blockDim.x + threadIdx.x;
    // Dot product
    int64_t dp = 0;
    for (uint j = 0; j < n; j++) dp += table[i * j % n] * vals[j] % modulus;
    dp %= modulus;
    result[i] = dp;
}

extern "C" __global__ void b(int64_t* p1, const int64_t* p2, uint degree, int64_t modulus) {
    uint i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < degree) {
        p1[i] += p2[i];
        p1[i] %= modulus;
    }
}

extern "C" __global__ void c(int64_t* p1, const int64_t* p2, uint degree, int64_t modulus) {
    uint i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < degree) {
        p1[i] *= p2[i];
        p1[i] %= modulus;
    }
}

extern "C" __global__ void d(int64_t* poly, int64_t* phi, uint n, int64_t inverse_n, int64_t modulus) {
    uint i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) {
        poly[i] *= inverse_n * phi[i] % modulus;
        poly[i] %= modulus;
    }
}