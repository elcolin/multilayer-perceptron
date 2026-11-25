# **************************************************************************** #
#                             multilayer-perceptron                            #
# **************************************************************************** #

# ---------------------------------- C++ ------------------------------------- #

NAME		:= mlp

CXX			:= c++
CXXFLAGS	:= -Wall -Wextra -Werror -std=c++17
CPPFLAGS	:= -Iinclude
DEPFLAGS	:= -MMD -MP

SRC_DIR		:= src
OBJ_DIR		:= obj

SRCS		:= main.cpp \
			   dataset.cpp \
			   perceptron.cpp

OBJS		:= $(addprefix $(OBJ_DIR)/, $(SRCS:.cpp=.o))
DEPS		:= $(OBJS:.o=.d)

# --------------------------------- Tests ------------------------------------ #

TEST_NAME	:= mlp_tests
TEST_DIR	:= tests/cpp
TEST_OBJ_DIR:= $(OBJ_DIR)/tests

DOCTEST		:= include/doctest.h
DOCTEST_URL	:= https://raw.githubusercontent.com/doctest/doctest/v2.4.11/doctest/doctest.h

TEST_SRCS	:= $(wildcard $(TEST_DIR)/*.cpp)
TEST_OBJS	:= $(patsubst $(TEST_DIR)/%.cpp, $(TEST_OBJ_DIR)/%.o, $(TEST_SRCS))
LIB_OBJS	:= $(filter-out $(OBJ_DIR)/main.o, $(OBJS))
DEPS		+= $(TEST_OBJS:.o=.d)

# --------------------------------- Python ----------------------------------- #

VENV		:= .venv
PYTHON		:= $(VENV)/bin/python
PIP			:= $(VENV)/bin/pip
REQS		:= requirements.txt

PLOT		:= scripts/plot.py
METRICS		:= output/metrics.csv

# --------------------------------- Display ---------------------------------- #

GREEN		:= \033[0;32m
BLUE		:= \033[0;34m
YELLOW		:= \033[0;33m
RESET		:= \033[0m

# ---------------------------------- Rules ----------------------------------- #

all: $(NAME)

$(NAME): $(OBJS)
	@$(CXX) $(CXXFLAGS) $(OBJS) -o $@
	@printf "$(GREEN)✔ $(NAME) compiled$(RESET)\n"

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp | $(OBJ_DIR)
	@$(CXX) $(CXXFLAGS) $(CPPFLAGS) $(DEPFLAGS) -c $< -o $@
	@printf "$(BLUE)  compiling$(RESET) $<\n"

$(OBJ_DIR):
	@mkdir -p $@

# Test binary: project objects (without main.o) + test objects
$(TEST_NAME): $(LIB_OBJS) $(TEST_OBJS)
	@$(CXX) $(CXXFLAGS) $^ -o $@
	@printf "$(GREEN)✔ $(TEST_NAME) compiled$(RESET)\n"

$(TEST_OBJ_DIR)/%.o: $(TEST_DIR)/%.cpp | $(DOCTEST)
	@mkdir -p $(dir $@)
	@$(CXX) $(CXXFLAGS) $(CPPFLAGS) $(DEPFLAGS) -c $< -o $@
	@printf "$(BLUE)  compiling$(RESET) $<\n"

# doctest single header, fetched once
$(DOCTEST):
	@curl -fsSL $(DOCTEST_URL) -o $@
	@printf "$(GREEN)✔ doctest downloaded$(RESET)\n"

# Python virtual environment, rebuilt only when requirements.txt changes
$(VENV): $(REQS)
	@python3 -m venv $(VENV)
	@$(PIP) install --quiet -r $(REQS)
	@touch $(VENV)
	@printf "$(GREEN)✔ python environment ready$(RESET)\n"

venv: $(VENV)

plot: $(VENV)
	@$(PYTHON) $(PLOT) $(METRICS)

test: test_cpp test_py

test_cpp: $(TEST_NAME)
	@./$(TEST_NAME)

test_py: $(VENV)
	@$(PYTHON) -m pytest

clean:
	@rm -rf $(OBJ_DIR)
	@printf "$(YELLOW)✘ objects removed$(RESET)\n"

fclean: clean
	@rm -f $(NAME) $(TEST_NAME)
	@printf "$(YELLOW)✘ $(NAME) removed$(RESET)\n"

vclean:
	@rm -rf $(VENV)
	@printf "$(YELLOW)✘ python environment removed$(RESET)\n"

re: fclean all

-include $(DEPS)

.PHONY: all clean fclean vclean re venv plot test test_cpp test_py
