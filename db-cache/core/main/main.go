package main

import (
	"fmt"
	"cache/core"
)

func main() {
	cli := core.ParseAppCli()
	config := core.ParseConfig(cli.ConfigFile)
	fmt.Printf("%v\n", config)
}
