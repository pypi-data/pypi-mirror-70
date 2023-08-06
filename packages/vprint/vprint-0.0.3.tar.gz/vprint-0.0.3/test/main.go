package main

import (
	"fmt"
	vprint2 "github.com/xkortex/vprint"
)

func main() {
	fmt.Println("test_start")
	vprint2.Print("[Hello, world!]")
	vprint2.Printf("[Hello, %s!]", "Printf")
	vprint2.Println("[Hello, Println!]")
	fmt.Println(vprint2.Blue("blue ", " color"))
	fmt.Println("test_end")
}
