# learnlib-py4j-example

This example shows how to learn a python-based system under learning (SUL) using [LearnLib][learnlib].

This example is a *python-first* example, meaning the core of our setup is written in Python and we use [Py4J][py4j] in order to use the Java based LearnLib from our Python program.

If you want a *java-first* approach, you may look into technologies such as [Jython][jython] which allows you to run Python programs on the JVM. If you want to go deeper down that rabbit hole, [GraalVM][graal] may be worth a look as well.


## Requirements

In order to run the Java side of the example you need to have a working [JDK][jdk] 8+ installation.
OpenJDK should work just as well as OracleJDK.
Furthermore, we use [Maven][maven] in order to build our LearnLib-Py4J connector.

---

For the Python side of this example you need to have a working [Python][python] installation.
The example has only been tested with Python3 - Python2 may or may not work.
We strongly suggest to install the [`virtualenv`][venv] tool in order to setup the Python side of Py4J without affecting your global Python installation - although technically you only need to have the `python-py4j` libraries installed somewhere.

---

In order to show the learned hypothesis automata, we suggest to install [GraphVIZ][graphviz].
However, if GraphVIZ (more specifically, `DOT`) is not installed, LearnLib will fallback to the [JUNG][jung] library, which is a fully Java-based visualization approach.


## Preparing the example


First, we will build the Java side of this example, which will leave us with an executable JAR containing the LearnLib and Py4J code.

```
cd java
mvn package
cd ..
```

---

Then, we setup our virtual python environment and install the py4j libraries

```
virtualenv python/venv
source python/venv/bin/activate
pip install py4j==0.10.8.1
```

## Running the example

To run the example, we first start our JVM process that listens for any calls performed by our Python programm (via the Py4J framework):

`java -jar java/target/learnlib-py4j-example-1.0-SNAPSHOT.jar`

---

Then, we simply run our Python program:

`python python/Main.py`

---

Once we are finished, the JVM process can be terminated by pressing <kbd>Ctrl</kbd> + <kbd>C</kbd> 


[learnlib]: https://github.com/LearnLib/learnlib
[py4j]: https://www.py4j.org/
[jython]: http://www.jython.org/
[graal]: https://www.graalvm.org/
[jdk]: https://www.oracle.com/technetwork/java/javase/overview/index.html
[maven]: https://maven.apache.org/
[python]: https://www.python.org/
[venv]: https://virtualenv.pypa.io
[graphviz]: http://www.graphviz.org/
[jung]: http://jung.sourceforge.net/
