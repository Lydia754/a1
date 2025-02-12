"""
Functions for extracting info from text formatted like Bluesky author "pages".
(CS 1110 assignment)


Author:   >>>>>> PUT YOUR NAME(S) AND NETID(S) HERE <<<<<<<<<<<
    Skeleton: Lillian Lee (LJL2)
Version: >>>>>> PUT COMPLETION DATE HERE <<<<<<<<<<<
    Skeleton: Feb 8, 2025
"""
import protect_students


def behead(s, marker):
    """
    Returns the part of s after the 1st occurrence of `marker`

    Case matters. The part returned can be empty.

    Example:
        behead('AXyx1x23', 'x')  ---> '1x23'
        behead('AXyx1x23', '3')  ---> ''

    s: a string containing marker
    marker: non-empty string
    """
    pass  # STUDENTS: replace with your implementation


def extract(s, left_marker, right_marker):
    """
    Returns the part of s between 1st left_marker and next non-overlapping right_marker

    Case matters. The part returned can be empty.

    Example:
        extract('AxyzB', 'A', 'B')  ---> 'xyz'
        extract('1112 1110 ? 1112 ', '1110', '1112') ---> ' ? '
        extract('AxyzB', 'A', 'x') ---> ''
        extract('ababaxyz', 'ab', 'ba') ---> 'a'

    s: a string containing both left_marker and right_marker.
        There's a right_marker in s after the 1st left_marker that doesn't overlap
        the first left_marker.
    left_marker: a non-empty string
    right_marker: a non-empty string
    """
    protect_students.pre_check_for_extract(left_marker, 'left_marker')
    protect_students.pre_check_for_extract(right_marker, 'right_marker')

    pass    # STUDENTS: replace with your implementation.
            # Your code must rely on calling behead()


def post_info(bp):
    """
    Returns: a string with the number of likes and text of post bp

    Format: '<N_LIKES> likes for: <TEXT>'


    bp: a string formatted as:

    ...data-testid="postText"STYLE>TEXT</div>...<button aria-label="Like (N_LIKES like...

    where STYLE, TEXT, N_LIKES are placeholders:
        STYLE doesn't contain any '>', can be empty
        TEXT doesn't contain '</div>', can be empty
        N_LIKES is not empty, is only digits, first digit is not 0
        ... stands for anything

    The following substrings occur in bp exactly once:
        data-testid="postText"
        <button aria-label="Like (

    Example: if bp were the string
      'h"data-testid="postText">hi</div>ab<button aria-label="Like (1110 likes)3'
    then this function returns the string
      1110 likes for: hi
    """
    # STUDENTS:
    # Your code must make effective use of at least one call to extract()
    # Please don't use all-caps for variable names.

    pass  # STUDENTS: replace with your implementation
