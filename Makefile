RANGE_DIR      ?= .
BASE_TEST_DIR  := ./test
BASE_PROJ_DIR  := ./pji
RANGE_TEST_DIR := ${BASE_TEST_DIR}/${RANGE_DIR}
RANGE_PROJ_DIR := ${BASE_PROJ_DIR}/${RANGE_DIR}

MIN_COVERAGE_CMD := $(if ${MIN_COVERAGE},--cov-fail-under=${MIN_COVERAGE},)

test: unittest

unittest:
		pytest "${RANGE_TEST_DIR}" \
			-sv -m unittest \
			--cov-report term-missing --cov="${RANGE_PROJ_DIR}" \
			${MIN_COVERAGE_CMD}