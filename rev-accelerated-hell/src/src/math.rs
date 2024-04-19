pub fn pow(mut val: i64, mut e: i64, modulus: i64) -> i64 {
    let mut res = 1;
    while e > 0 {
        if (e & 1) == 1 {
            res = res * val % modulus;
        }
        e >>= 1;
        val = val * val % modulus;
    }
    return res;
}

pub fn inverse(val: i64, modulus: i64) -> i64 {
    return pow(val, modulus - 2, modulus);
}
