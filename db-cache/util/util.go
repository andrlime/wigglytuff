package util

import (
	"errors"
	"fmt"
)

func WrapError(context string, err error) error {
	return errors.New(fmt.Sprintf("[%s] %s", context, err))
}

func CreateError(context string, errorMsg string) error {
	return errors.New(fmt.Sprintf("[%s] %s", context, errors.New(errorMsg)))
}
