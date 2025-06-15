package core

import (
	"flag"
	"sync"
)

type CliConfig struct {
	ConfigFile string
}

var (
	cliConfig *CliConfig
	cliOnce   sync.Once
)

func ParseAppCli() *CliConfig {
	cliOnce.Do(func() {
		cliConfig = &CliConfig{}
		config_file := flag.String("config", "config.yaml", "path to the config.yml/yaml file")
		flag.Parse()
		cliConfig.ConfigFile = *config_file
	})

	return cliConfig
}
