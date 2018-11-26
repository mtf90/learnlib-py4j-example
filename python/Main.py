from py4j.java_gateway import JavaGateway, CallbackServerParameters


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
    gateway = JavaGateway(callback_server_parameters=CallbackServerParameters())

    sul = PySUL(gateway)
    alphabet = sul.alphabet

    mq_oracle = gateway.jvm.de.learnlib.oracle.membership.SULOracle(sul)
    eq_oracle = gateway.jvm.de.learnlib.oracle.equivalence.WMethodEQOracle(mq_oracle, 3)

    ttt = gateway.jvm.de.learnlib.algorithms.ttt.mealy.TTTLearnerMealyBuilder() \
        .withAlphabet(alphabet) \
        .withOracle(mq_oracle) \
        .create()

    experiment = gateway.jvm.de.learnlib.util.Experiment(ttt, eq_oracle, alphabet)
    experiment.run()

    hyp = experiment.getFinalHypothesis()

    string_writer = gateway.jvm.java.io.StringWriter()

    gateway.jvm.net.automatalib.serialization.dot.GraphDOT.write(hyp, alphabet, string_writer,
                                                                 # While varargs allow us to skip this parameter in Java, the method signature expects an array \
                                                                 gateway.new_array(
                                                                     gateway.jvm.net.automatalib.serialization.dot.DOTVisualizationHelper,
                                                                     0))

    print("Learned model in DOT format:")
    print()
    print(string_writer.toString())

    gateway.jvm.net.automatalib.visualization.Visualization.visualize(hyp, alphabet,
                                                                      # While varargs allow us to skip this parameter in Java, the method signature expects an array \
                                                                      gateway.new_array(
                                                                          gateway.jvm.net.automatalib.visualization.VisualizationHelper,
                                                                          0))

    gateway.close()


if __name__ == "__main__":
    main()
