use std::io::{self, Write};
use parallel_fft::algo::fft_algo::*;
use parallel_fft::algo::gpu_1d_nc::*;
use parallel_fft::params::*;

const PARAMS : Params = Params {
    degree: 1 << 8,
    modulus: 557057, // 17 * 2^15 + 1
    root: 439666,
};

const CORRECT : [i64; PARAMS.degree] = [433205, 457895, 479205, 502267, 522707, 544889, 15380, 42142, 67078, 94300, 115568, 143734, 169562, 197160, 219316, 245274, 268354, 294982, 318476, 343712, 368638, 393508, 417288, 446676, 475006, 499430, 525850, 553248, 23283, 54193, 84563, 111807, 137705, 167921, 199907, 231869, 258645, 286643, 319483, 348171, 376285, 404077, 424319, 448045, 469347, 497751, 531247, 8688, 42904, 77608, 98870, 112518, 149968, 157998, 163468, 168938, 174408, 179878, 185348, 190818, 196288, 201758, 207228, 212698, 218168, 223638, 229108, 234578, 240048, 245518, 250988, 256458, 261928, 267398, 272868, 278338, 283808, 289278, 294748, 300218, 305688, 311158, 316628, 322098, 327568, 333038, 338508, 343978, 349448, 354918, 360388, 365858, 371328, 376798, 382268, 387738, 393208, 398678, 404148, 409618, 415088, 420558, 426028, 431498, 436968, 442438, 447908, 453378, 458848, 464318, 469788, 475258, 480728, 486198, 491668, 497138, 502608, 508078, 513548, 519018, 524488, 529958, 535428, 540898, 546368, 551838, 251, 5721, 11191, 16661, 22131, 27601, 33071, 38541, 44011, 49481, 54951, 60421, 65891, 71361, 76831, 82301, 87771, 93241, 98711, 104181, 109651, 115121, 120591, 126061, 131531, 137001, 142471, 147941, 153411, 158881, 164351, 169821, 175291, 180761, 186231, 191701, 197171, 202641, 208111, 213581, 219051, 224521, 229991, 235461, 240931, 246401, 251871, 257341, 262811, 268281, 273751, 279221, 284691, 290161, 295631, 301101, 306571, 312041, 317511, 322981, 328451, 333921, 339391, 344861, 350331, 355801, 361271, 366741, 372211, 377681, 383151, 388621, 394091, 399561, 405031, 410501, 415971, 421441, 426911, 432381, 437851, 443321, 448791, 454261, 459731, 465201, 470671, 476141, 481611, 487081, 492551, 498021, 503491, 508961, 514431, 519901, 525371, 530841, 536311, 541781, 547251, 552721, 1134, 6604, 12074, 17544, 23014, 28484, 33954, 39424, 44894, 50364, 55834, 61304, 66774, 72244, 77714, 83184, 88654, 94124, 99594, 105064, 110534, 116004, 121474, 126944, 132414, 137884, 143354, 148824];

fn main() -> io::Result<()> {
    //Quick-init GPU contexts for everything
    let _context = rustacuda::quick_init().unwrap();
    print!("Flag: ");
    io::stdout().flush()?;
    let mut input = String::new();
    io::stdin().read_line(&mut input)?;
    let bytes = input.into_bytes();
    if bytes.len() != 54 {
        println!("Nope!");
        return Ok(())
    }
    let mut p: Vec<i64> = bytes.into_iter().map(|b| (b as i64) % PARAMS.modulus).collect();
    p.resize(PARAMS.degree, 0);
    let mut p2: Vec<i64> = vec![0; PARAMS.degree];
    let mut p3: Vec<i64> = vec![0; PARAMS.degree];
    for i in 0..PARAMS.degree {
        p2[i] = ((i as i64) + 1) % PARAMS.modulus;
        p3[i] = ((PARAMS.degree as i64) - (i as i64)) % PARAMS.modulus;
    }
    
    // Initialization
    let mut fft = GPUFFT1DNC::new(PARAMS);
    let mut poly = fft.from_coeffs(p);
    let x2 = fft.from_coeffs(p2);
    poly = fft.mul(poly, x2);
    let x3 = fft.from_coeffs(p3);
    poly = fft.add(poly, x3);

    let res_p = fft.to_coeffs(poly);
    
    if res_p.as_slice() == CORRECT {
        println!("Correct!")
    } else {
        println!("Nope!")
    }
    Ok(())
}