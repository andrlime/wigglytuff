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
		Username	string	`env:"RABBITMQ_USERNAME"`
		Password	string	`env:"RABBITMQ_PASSWORD"`
	}

	RabbitMqConfig struct {
		RabbitMqQueueName	string	`yaml:"queue_name"`
		RabbitMqHostname	string	`yaml:"hostname"`
		RabbitMqPort		int		`yaml:"port"`
	}	`yaml:"rabbitmq"`
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

func ParseConfig(configFile string) *AppConfig {
	appCfgOnce.Do(func() {
		appConfig = &AppConfig{}
		appConfig.ParseAppEnv()
		appConfig.ParseYamlConfig(configFile)
	})
	return appConfig
}
