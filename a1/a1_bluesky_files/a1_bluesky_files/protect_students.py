"""
Help students avoid a subtle problem about empty strings as markers when
extracting.

We've written preconditions that rule out empty-string markers, but it could
be easy for students to miss those preconditions.  

Author: Lillian Lee (LJL2)
Version: Feb 8, 2025
"""
import a1_second


def pre_check_for_extract(s, var_name):
    """Raises an AssertionError if s is the empty string

    s is a string
    var_name is a string
    """
    msg = ('Function extract() is called somewhere in student-written code '
           + 'with an empty string for ' + var_name + '\n'
           + 'Dear CS1110 student, '
           + 'figure out why doing so is a conceptual mistake!\n')
    assert len(s) > 0, msg


def test_extract_safeguards():
    """Ensure safeguard lines not removed"""

    progress_msg = "a1_second.extract() still has staff-written safeguards"
    print("Testing "+progress_msg)

    msg=('\nDear CS1110 student:\n'
         + "please restore one or both of the following lines "
         + "to the start of extract()\n"
         + "\tprotect_students.pre_check_for_extract(left_marker, 'left_marker')\n"
         + "\tprotect_students.pre_check_for_extract(right_marker,"
         +" 'right_marker')\n"
         +"Quitting testing now\n"
         +"^^^ Repair extract() before proceeding.^^^\n")

    for (lm, rm) in [('', 't'), ('t', '')]:
        try:
            a1_second.extract('test', lm, rm)
        except AssertionError:
            pass
        else:
            exit(msg)

    print("Completed testing that " + progress_msg)
