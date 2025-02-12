"""
Tests for code for processing Bluesky posts
(CS 1110 assignment)


Author:   >>>>>> PUT YOUR NAME(S) AND NETID(S) HERE <<<<<<<<<<<
    Skeleton: Lillian Lee (LJL2), Adeniyi Fagbewesa (amf349)
Version: >>>>>> PUT COMPLETION DATE HERE <<<<<<<<<<<
    Skeleton: Feb 6, 2025
"""

# STUDENTS:
# Read assignment writeup before proceeding!
#
# Throughout, we use parentheses to enclose multi-line string concatenations.

import cornellasserts
import a1_second
import protect_students


def test_behead():
    """ Test a1_second.behead() """
    print("Testing a1_second.behead()")

    # STUDENTS: see instructions in assignment writeup!!!

    # 1. Two occurrences of marker, mixed case
    # Guaranteed correct
    result = a1_second.behead("AXyx1x23", "x")
    cornellasserts.assert_equals('1x23', result)

    # 2. marker not in s
    # ... STUDENT-DELETED CASE ...
    # 
    result = a1_second.behead('start', 'x')
    cornellasserts.assert_equals('start', result)

    # 3. parts of marker occur before full marker
    result = a1_second.behead('start the cart, Bart', 'cart')
    cornellasserts.assert_equals(', Bart', result)

    # 4. ditto, but marker is longer
    result = a1_second.behead('start the cart, Bart', ' cart')
    cornellasserts.assert_equals('Bart', result)

    # 5. ditto, but front of marker occurs beforehand
    result = a1_second.behead('start the starter, Bart', 'starter')
    cornellasserts.assert_equals(', Bart', result)

    # STUDENTS: add any missing representative test cases below

    print("Completed testing a1_second.behead()")


def test_extract():
    """ Test a1_second.extract() """
    print("Testing a1_second.extract()")

    # STUDENTS: see instructions in assignment writeup!!!

    # 1. Markers at ends
    # Guaranteed correct
    result = a1_second.extract('AxyzB', 'A', 'B')
    cornellasserts.assert_equals('xyz', result)

    # 2. A right_marker before left_marker, spaces in extracted part
    result = a1_second.extract('1112 1110 ? 1112 ', '1110', '1112')
    cornellasserts.assert_equals('?', result)

    # 3. Adjacent markers.
    # Guaranteed correct
    result = a1_second.extract('AxyzB', 'A', 'x')
    cornellasserts.assert_equals('', result)

    # 4. Some marker overlap, multiletter markers
    # Guaranteed correct
    result = a1_second.extract('ababaxyz', 'ab', 'ba')
    cornellasserts.assert_equals('a', result)

    # 5. Check that case matters
    result = a1_second.extract('axyzBZZ123ApqrbzBzzz', 'A', 'Bzz')
    cornellasserts.assert_equals('pqrbz', result)

    # STUDENTS: add any missing representative test cases below


    print("Completed testing a1_second.extract()")


def test_post_info():
    """ Test a1_second.post_info() """

    print("Testing a1_second.post_info()")

    # 1. Very simple version of template
    # Guaranteed correct
    ts = ('<div>bla<h"data-testid="postText"aBc>here I am!</div>'
          +'1233<button aria-label="Like (1110 likes)"here is more text')
    result = a1_second.post_info(ts)
    cornellasserts.assert_equals('1110 likes for: here I am!', result)

    # 2. Pieces of tags are in TEXT or STYLES, pieces of marker exist throughout
    # Guaranteed correct
    ts = ('id="postText"not really post text'
          + '<div>blah<"data-testid="postText"aBc>here"data-testid=I am!</</div>'
          + '  a s<dif>button aria-label="fancy"'
          + '<button aria-label=Like (14 likes) <button aria-label="Like (25 likes)'
          )
    result = a1_second.post_info(ts)
    cornellasserts.assert_equals('25 likes for: here"data-testid=I am!</', result)

    # 3. More pieces of tags in TEXT, STYLES empty, back ends of markers throughout
    # Guaranteed correct
    ts = (
        '"postText"=jkl>iopdata-testid="postText">voiv>la</div>123'
        + '=Like 21 test test aria-label="Like (N_LIKES asds'
        + '<button aria-label="Like (123456 likes)" font-variant'
    )
    result = a1_second.post_info(ts)
    cornellasserts.assert_equals('123456 likes for: voiv>la', result)

    # 4. Empty TEXT
    # Guaranteed correct
    ts = ('<div>bla<h"data-testid="postText"aBc></div>'
          + '1233<<button aria-label="Like (1 like)"')
    result = a1_second.post_info(ts)
    cornellasserts.assert_equals('1 likes for: ', result)

    # STUDENTS: add any missing representative test cases below


    print("Completed testing a1_second.post_info()")


###########
# Calls to testing functions
###########

# Code below executed only if this file is run as a script
# (as opposed to imported).
if __name__ == '__main__':

    keep_going = True
    test_behead()
    protect_students.test_extract_safeguards()  # Staff-written function
    test_extract()
    test_post_info()

    print('\nPassed all tests in this file. Hurrah!')
    print('But, make sure you also added enough tests')
