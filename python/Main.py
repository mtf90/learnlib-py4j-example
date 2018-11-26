from py4j.java_gateway import JavaGateway, CallbackServerParameters

# This class represents the Python side implementation of our system under learning (SUL)
class PySUL:

    def __init__(self, gateway):
        self.alphabet = gateway.jvm.net.automatalib.words.impl.Alphabets.characters('a', 'b')
        self.state = 0

    def pre(self):
        self.state = 0

    def post(self): pass

    def step(self, sulInput):
        if sulInput == 'b':
            self.state = (self.state + 1) % 2
            return 'b'

        return '0' if self.state == 0 else '1'

    def canFork(self):
        return False

    def fork(self): pass

    class Java:
        implements = ["de.learnlib.api.SUL"]


def main():
    # Create our connection to the JVM process
    gateway = JavaGateway(callback_server_parameters=CallbackServerParameters())

    # Instantiate our Python SUL and get the learning alphabet
    sul = PySUL(gateway)
    alphabet = sul.alphabet

    # Construct the membership oracle
    mq_oracle = gateway.jvm.de.learnlib.oracle.membership.SULOracle(sul)

    # Construct the equivalence oracle
    eq_oracle = gateway.jvm.de.learnlib.oracle.equivalence.WMethodEQOracle(mq_oracle, 3)

    # Construct the learning algorithm (here TTT)
    ttt = gateway.jvm.de.learnlib.algorithms.ttt.mealy.TTTLearnerMealyBuilder() \
        .withAlphabet(alphabet) \
        .withOracle(mq_oracle) \
        .create()

    # Construct the experiment, that runs the active learning loop until no more counterexamples can be found.
    experiment = gateway.jvm.de.learnlib.util.Experiment(ttt, eq_oracle, alphabet)
    experiment.run()

    # Get the final hypothesis of our SUL
    hyp = experiment.getFinalHypothesis()

    # Construct a buffer that we will use to print results on the Python side of our setup
    string_writer = gateway.jvm.java.io.StringWriter()

    # Serialize the hypothesis to the DOT format and write it to the string_writer
    gateway.jvm.net.automatalib.serialization.dot.GraphDOT.write(hyp, alphabet, string_writer,
                                                                 # While varargs allow us to skip this parameter in Java, the method signature expects an array \
                                                                 gateway.new_array(
                                                                     gateway.jvm.net.automatalib.serialization.dot.DOTVisualizationHelper,
                                                                     0))

    print("Learned model in DOT format:")
    print()
    print(string_writer.toString())

    # Visualize the hypothesis
    gateway.jvm.net.automatalib.visualization.Visualization.visualize(hyp, alphabet,
                                                                      # While varargs allow us to skip this parameter in Java, the method signature expects an array \
                                                                      gateway.new_array(
                                                                          gateway.jvm.net.automatalib.visualization.VisualizationHelper,
                                                                          0))

    # Close our connection
    gateway.close()


if __name__ == "__main__":
    main()
