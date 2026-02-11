package main

import "testing"

func TestBlocksBacktick(t *testing.T) {
	if SanitizeCommand("echo `whoami`") == nil { t.Error("should block") }
}
func TestAllowsSafe(t *testing.T) {
	if SanitizeCommand("ls -la /tmp") != nil { t.Error("should allow") }
}
