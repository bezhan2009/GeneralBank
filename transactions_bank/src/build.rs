fn main() {
    println!("cargo:rustc-link-search=native=C:/Program Files (x86)/sqlite3");
    println!("cargo:rustc-link-lib=dylib=sqlite3");
}
