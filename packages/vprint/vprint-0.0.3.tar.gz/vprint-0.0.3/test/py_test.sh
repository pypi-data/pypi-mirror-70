#!/usr/bin/env bash


errcho() {
    (>&2 echo -e "\e[31m$1\e[0m")
}

FAILED=

if [[ -n $(python -c "from vprint import vprint; vprint('nope')" 2>&1) ]]; then
  errcho "1. Saw output when nothing was expected"
  FAILED=1
fi


if [[ -n $(VPRINTV=1 python -c "from vprint import vprint; vprint('stderr_only')" 2>/dev/null) ]]; then
  errcho "2. Saw output on stdout when none was expected"
  FAILED=1
fi


if [[ -z $(VPRINTV=1 python -c "from vprint import vprint; vprint('yup')" 2>&1) ]]; then
  errcho "3. Saw no output when some was expected"
  FAILED=1
fi

if [[ -z $(VPRINTV=1 VPRINTV_FILE=stdout python -c "from vprint import vprint; vprint('yup')" 2>&1) ]]; then
  errcho "4. Saw no output when some was expected"
  FAILED=1
fi


if [[ -z $(VPRINTV=1 python -c "from vprint import vprint; vprint('yup')" 2>&1 1>/dev/null) ]]; then
  errcho "5. Expected to see stderr, did not see anything"
  FAILED=1
fi


if [[ -n $(VPRINTV=1 python -c "from vprint import vprint; vprint('yup')" 2>/dev/null ) ]]; then
  errcho "6. Expected to see stderr, did not see anything"
  FAILED=1
fi


if [[ -n $(VPRINTV=1 VPRINTV_FILE=stdout python -c "from vprint import vprint; vprint('nope')" 2>&1 1>/dev/null) ]]; then
  errcho "7. Routed stdout, but saw output in stderr"
  FAILED=1
fi


if [[ -z $(VPRINTV=1 VPRINTV_FILE=stdout python -c "from vprint import vprint; vprint('yup')"  ) ]]; then
  errcho "8. Expected to see stout, did not see anything"
  FAILED=1
fi


TMPOUT=$(VPRINTV=1 VPRINTV_FILE=/tmp/vprinttest.log python -c "from vprint import vprint; vprint('to file')" 2>&1)
if [[ $? -ne 0 ]]; then
  errcho "9a. Routed to file, but process exited with error"
fi
if [[ -n "${TMPOUT}" ]]; then
  errcho "9b. Routed to file, but saw output in stdout/err"
  FAILED=1
fi

if [[ -z "$(cat /tmp/vprinttest.log)" ]]; then
  errcho "9c. Routed to file, but file was empty"
  FAILED=1
fi

rm -rf /tmp/vprinttest.log



if [[ -n "$FAILED" ]]; then
  echo "Failed one or more tests"
  exit 1
fi

echo "PASS!"