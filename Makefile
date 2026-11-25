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
			   perceptron.cpp

OBJS		:= $(addprefix $(OBJ_DIR)/, $(SRCS:.cpp=.o))
DEPS		:= $(OBJS:.o=.d)

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

# Python virtual environment, rebuilt only when requirements.txt changes
$(VENV): $(REQS)
	@python3 -m venv $(VENV)
	@$(PIP) install --quiet -r $(REQS)
	@touch $(VENV)
	@printf "$(GREEN)✔ python environment ready$(RESET)\n"

venv: $(VENV)

plot: $(VENV)
	@$(PYTHON) $(PLOT) $(METRICS)

test: $(VENV)
	@$(PYTHON) -m pytest

clean:
	@rm -rf $(OBJ_DIR)
	@printf "$(YELLOW)✘ objects removed$(RESET)\n"

fclean: clean
	@rm -f $(NAME)
	@printf "$(YELLOW)✘ $(NAME) removed$(RESET)\n"

vclean:
	@rm -rf $(VENV)
	@printf "$(YELLOW)✘ python environment removed$(RESET)\n"

re: fclean all

-include $(DEPS)

.PHONY: all clean fclean vclean re venv plot test
