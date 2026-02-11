package main

import (
	"fmt"
	"strings"
)

var dangerousPatterns = []string{"`", "$(" , "||", "&&", ";", ">", "<"}

func SanitizeCommand(raw string) error {
	for _, p := range dangerousPatterns {
		if strings.Contains(raw, p) {
			return fmt.Errorf("blocked: dangerous pattern %q", p)
		}
	}
	return nil
}
