use crate::params::Params;

pub trait FftAlgorithm {
    type Polynomial;

    fn new(params: Params) -> Self;

    /// Conversion to/from coefficients.
    /// Note that it is assumed that `v` will be zero-padded to `params.degree` length.
    fn from_coeffs(&mut self, v: Vec<i64>) -> Self::Polynomial;
    fn to_coeffs(&mut self, poly: Self::Polynomial) -> Vec<i64>;

    /// Polynomial Operations
    fn add(&mut self, p1: Self::Polynomial, p2: Self::Polynomial) -> Self::Polynomial;
    fn mul(&mut self, p1: Self::Polynomial, p2: Self::Polynomial) -> Self::Polynomial;
}
