# Homework 4

Part 1 assumes you have an Object Calculus interpreter. For the course, they provided a binary that you could use, but that doesn't work for us. At least it doesn't work on my Mac.

Instead, I used Rylan's solution. But you can use mine.

    git checkout dev -- hw4/interpreter.py

Then you can test your own solution using:

    cd hw4
    python src/main_objc.py problem.objc problem_test.objc --verify problem.objc.golden

You can use the files in `test` to get a sense for how Object Calculus syntax works. Make sure not to look at `interpreter.py` since you'll implement it in Part 2!

To reset `interpreter.py` back to where it started once you're done:

    git checkout main -- hw4/interpreter.py
