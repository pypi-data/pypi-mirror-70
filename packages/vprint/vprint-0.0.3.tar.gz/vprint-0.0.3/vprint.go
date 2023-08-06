package vprint

import (
	"fmt"
	"io"
	"os"
	"strconv"
)

const (
	cBlack   = "\033[30m"
	cRed     = "\033[31m"
	cGreen   = "\033[32m"
	cYellow  = "\033[33m"
	cBlue    = "\033[34m"
	cMagenta = "\033[35m"
	cCyan    = "\033[36m"
	cWhite   = "\033[37m"
)

const (
	endColor = "\033[0m"
	endLine  = "\033[0m\n"
)

type vprintSettings struct {
	verbosity    int64
	useColor     bool
	w            io.Writer
	vprintColor  string
	debugColor   string
	infoColor    string
	noticeColor  string
	warningColor string
	errorColor   string
	print        func(a ...interface{})
	printf       func(format string, a ...interface{})
	println      func(a ...interface{})
}

var settings = &vprintSettings{
	verbosity:    0,
	useColor:     true,
	w:            os.Stderr,
	vprintColor:  cYellow,
	debugColor:   cYellow,
	infoColor:    cBlue,
	noticeColor:  cCyan,
	warningColor: cYellow,
	errorColor:   cRed,
}

var (
	Print   = nop
	Printf  = nopf
	Println = nop
)

func init() {

	settings.verbosity, _ = strconv.ParseInt(os.Getenv("VPRINTV"), 10, 16)
	out_writer := os.Getenv("VPRINT_OUT")
	if s := os.Getenv("VPRINT_NOCOLOR"); s != "" {
		settings.useColor = false
	}
	if settings.verbosity > 0 {
		Print = print
		Printf = printf
		Println = println
	}

	switch out_writer {
	case "Stdout":
		settings.w = os.Stdout
	case "Stderr":
	default:
		settings.w = os.Stderr

	}
}

func OptionColor(a ...interface{}) string {
	if settings.useColor {
		return fmt.Sprint(a...)
	}
	return fmt.Sprint(settings.vprintColor) + fmt.Sprint(a...) + fmt.Sprint(endColor)

}

func print(a ...interface{}) {
	if settings.useColor {
		fmt.Fprint(settings.w, settings.vprintColor)
	}
	fmt.Fprint(settings.w, a...)
	if settings.useColor {
		fmt.Fprint(settings.w, endColor)
	}

}
func printf(format string, a ...interface{}) {
	if settings.useColor {
		fmt.Fprint(settings.w, settings.vprintColor)
	}
	fmt.Fprintf(settings.w, format, a...)
	if settings.useColor {
		fmt.Fprint(settings.w, endColor)
	}

}

func println(a ...interface{}) {
	if settings.useColor {
		fmt.Fprint(settings.w, settings.vprintColor)
	}
	fmt.Fprintln(settings.w, a...)
	if settings.useColor {
		fmt.Fprint(settings.w, endColor)
	}

}

func nop(a ...interface{}) {
}

func nopf(format string, a ...interface{}) {
}

func Red(a ...interface{}) string {
	return fmt.Sprint(cRed) + fmt.Sprint(a...) + fmt.Sprint(endColor)
}

func Green(a ...interface{}) string {
	return fmt.Sprint(cGreen) + fmt.Sprint(a...) + fmt.Sprint(endColor)
}

func Blue(a ...interface{}) string {
	return fmt.Sprint(cBlue) + fmt.Sprint(a...) + fmt.Sprint(endColor)
}

func Yellow(a ...interface{}) string {
	return fmt.Sprint(cYellow) + fmt.Sprint(a...) + fmt.Sprint(endColor)
}

func Cyan(a ...interface{}) string {
	return fmt.Sprint(cCyan) + fmt.Sprint(a...) + fmt.Sprint(endColor)
}

func Magenta(a ...interface{}) string {
	return fmt.Sprint(cMagenta) + fmt.Sprint(a...) + fmt.Sprint(endColor)
}
