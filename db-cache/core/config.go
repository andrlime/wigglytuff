package core

import (
	"log"
	"os"
	"sync"

	"github.com/caarlos0/env/v11"
	"gopkg.in/yaml.v3"
)

type AppConfig struct {
	RabbitMqCredentials struct {
		Username string `env:"RABBITMQ_USERNAME"`
		Password string `env:"RABBITMQ_PASSWORD"`
	}

	RabbitMqConfig struct {
		QueueName string `yaml:"queue_name"`
		HostName  string `yaml:"hostname"`
		Port      uint16 `yaml:"port"`
	} `yaml:"rabbitmq"`
}

var (
	appConfig  *AppConfig
	appCfgOnce sync.Once
)

// Note that this does NOT load from .env. It loads from environment variables
// passed in via compose.yaml
func (cfg *AppConfig) ParseAppEnv() {
	if err := env.Parse(cfg); err != nil {
		log.Fatal(err)
	}
}

func (cfg *AppConfig) ParseYamlConfig(configFile string) {
	f, err := os.ReadFile(configFile)
	if err != nil {
		log.Fatal(err)
	}

	if err := yaml.Unmarshal(f, cfg); err != nil {
		log.Fatal(err)
	}
}

func ParseConfig() *AppConfig {
	cli := ParseAppCli()
	appCfgOnce.Do(func() {
		appConfig = &AppConfig{}
		appConfig.ParseAppEnv()
		appConfig.ParseYamlConfig(cli.ConfigFile)
	})
	return appConfig
}
