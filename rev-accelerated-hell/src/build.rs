//WARNING: This thing appears to not work if there's a bug in the cu code. Check with manual nvcc.

use std::fs;
use std::process::Command;

fn main() {
    println!("cargo:rerun-if-changed=src/cuda");

    let files = fs::read_dir("src/cuda").unwrap();
    fs::create_dir("ptx").unwrap_or_default();
    for f in files {
        let fobj = f.unwrap();
        let fname = &fobj.file_name().into_string().unwrap();
        Command::new("nvcc")
            .arg("-ptx")
            .arg("-o")
            .arg(format!("ptx/{}.ptx", fname))
            .arg(fobj.path().to_str().unwrap()).output().unwrap();
    }
}