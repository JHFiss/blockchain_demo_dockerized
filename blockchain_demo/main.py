
import computationnode


n0 = computationnode.ComputationNode("127.0.0.1", 8001, 'Testdata', 1)

n1 = computationnode.ComputationNode("127.0.0.1", 8002, 'Testdata', 2)

n2 = computationnode.ComputationNode("127.0.0.1", 8002, 'Testdata', 2)
# Schedule three calls *concurrently*:

n0.start()
n1.start()
n2.start()

n1.connect_with_node('127.0.0.1', 8001)
n2.connect_with_node('127.0.0.1', 8001)
n2.connect_with_node('127.0.0.1', 8002)

n0.add_new_data('Testdata1')
n1.add_new_data('Testdata2')
n0.add_new_data('Testdata3')
n1.add_new_data('Testdata4')
n2.add_new_data('Testdata5')
n2.add_new_data('Testdata6')

print(str(n0.my_blockchain))
print(str(n1.my_blockchain))
print(str(n2.my_blockchain))

n0.stop()
n1.stop()
n2.stop()




