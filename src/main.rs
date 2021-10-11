fn main() {
    //println!("Hello, world!");
    let a = String::from("hello");
    let b = String::from(" world");
    let t = [a,b];
    for i in t.iter(){
        println!("{}",i)
    }

}
