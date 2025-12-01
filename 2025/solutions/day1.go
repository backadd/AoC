package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

func main() {
	filename := filepath.Join("..", "inputs", "day1.txt")
	data, err := os.ReadFile(filename)
	if err != nil {
		panic(err)
	}

	lines := strings.Split(string(data), "\n")
	// Remove empty last line if file ends with \n
	if len(lines) > 0 && lines[len(lines)-1] == "" {
		lines = lines[:len(lines)-1]
	}

	dial := 50 // this is the starting value
	count := 0
	secondCount := 0

	for i, line := range lines {
		timesPassedZero := 0
		if line == "" {
			continue
		}
		fmt.Printf("Line %d: %s → ", i+1, line)
		dial, timesPassedZero = turnDial(dial, line) // ← must assign returned value!
		secondCount += timesPassedZero
		fmt.Println("Now at:", dial)
		if dial == 0 {
			count++
		}
	}

	fmt.Printf("Final count value: %d\n", count)
	fmt.Printf("Final count value: %d\n", secondCount)
}

func turnDial(dial int, instruction string) (newDial int, timesPassedZero int) {
	timesPassedZero = 0

	if len(instruction) < 1 {
		fmt.Println("Warning: empty or too short instruction:", instruction)
		return dial, timesPassedZero
	}

	direction := strings.ToLower(string(instruction[0])) // "l" or "r"
	numStr := instruction[1:]                            // FIXED: was `s[1:]` → typo!
	number, err := strconv.Atoi(numStr)
	if err != nil {
		fmt.Println("Warning: invalid number in:", instruction)
		return dial, timesPassedZero
	}

	// Validate direction
	if direction != "l" && direction != "r" {
		fmt.Printf("ERROR: invalid direction '%s' in '%s'\n", direction, instruction)
		return dial, timesPassedZero // or panic, or return error
	}

	// Apply the movement 'number' times
	for i := 0; i < number; i++ {
		if direction == "l" {
			if dial == 0 {
				dial = 99
			} else {
				dial--
			}
		} else { // "r"
			if dial == 99 {
				dial = 0
			} else {
				dial++
			}
		}
		if dial == 0{
			timesPassedZero++
		}
	}

	return dial, timesPassedZero // ← must return the updated value!
}
