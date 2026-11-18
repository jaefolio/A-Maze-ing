*This project has been created as part of the 42 curriculum by zetan.*

## Description
Get Next Line is a project that involves retrieving a single line based on the '\n' character from a given file descriptor. The goal of this project is to discover on a new concept called static variables, which is essentially just variables that are able to maintain their values across multiple function calls, as long as the program is still running.

## Instructions
To compile the `get_next_line` into an executable. Run the following command: 
	* `cc -Wall -Wextra -Werror get_next_line.c get_next_line_utils.c`

And for the bonus, run:
	* `cc -Wall -Wextra -Werror get_next_line_bonus.c get_next_line_bonus_utils.c`

## Resources
**Online Resources**
	* Static Variables - https://www.geeksforgeeks.org/c/static-variables-in-c/

**Manual**
	* Read - https://man7.org/linux/man-pages/man2/read.2.html
	* Open - https://man7.org/linux/man-pages/man2/open.2.html

**AI Used**
AI was used in this project to clarify concepts and assist in debugging code.
	* Concepts such as how read and open works, and how to utilize static variables.
	* Test for bugs with certain edge cases (e.g. not returning NULL when the stash is empty)
