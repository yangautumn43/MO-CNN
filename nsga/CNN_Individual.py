## CNN_Individual.py
##
##

import random

from CNN_Gene import *
from pyNSGAII import AbstractIndividual


"""
# Helper functions --- Genotypes will implement one set of generators
# randomly generate a ConvGene based on the lastGene's output dimension
"""
def generate1DConvGene(lastGene, nextGene):
	## specify the min and max for each random functions

	# What are the boundaries of this gene (input and output size)
	input_size = lastGene.outputDimension()[0]
	min_output_size = nextGene.minInputDimension()[0]

	# If the next layer is FC or output, then the output can be length of 1
	if len(nextGene.minInputDimension()) == 1:
		min_output_size = 1

	# Figure out the range of sizes for the kernel
	min_size = MIN_CNN_WIDTH
	max_size = MAX_CNN_WIDTH

	# The maximum the kernel can be is
	# input_size - min_output_size + 1
	max_size = min(MAX_CNN_WIDTH, input_size - min_output_size + 1)

	if max_size < MIN_CNN_WIDTH:
		return None

	kernel_size = np.random.randint(MIN_CNN_WIDTH, max_size+1)

	# The stride can be up to
	# ((input_size - kernel_size + 1) / min_output_size) + 1
	max_stride = ((input_size - kernel_size + 1) / min_output_size) + 1
	max_stride = min(MAX_CNN_STRIDE, max_stride)

	# Stride can also not exceed the kernel size
	max_stride = min(max_stride, kernel_size)

	if max_stride < MIN_CNN_STRIDE:
		return None

	conv_stride = np.random.randint(MIN_CNN_STRIDE, max_stride+1)

	# Can have any number of kernels
	num_kernels = np.random.randint(MIN_CNN_KERNELS, MAX_CNN_KERNELS+1)

	# activation_function ???
	return Conv1DGene((kernel_size,), (conv_stride,), num_kernels, activation_function=None)


def generate2DConvGene(lastGene, nextGene):
	## specify the min and max for each random functions

	# What are the boundaries of this gene (input and output size)

	input_height, input_width, _ = lastGene.outputDimension()
	min_output_size = nextGene.minInputDimension()

	min_output_height = 1
	min_output_width = 1

	if len(min_output_size) > 1:
		min_output_height = min_output_size[0]
		min_output_width = min_output_size[1]

	min_height = MIN_CNN_WIDTH
	min_width = MIN_CNN_WIDTH

	# The maximum the kernel can be in either direction is
	# input_size - min_output_size + 1
	max_height = min(MAX_CNN_WIDTH, input_height - min_output_height + 1)
	max_width = min(MAX_CNN_WIDTH, input_width - min_output_width + 1)

	if max_height < MIN_CNN_WIDTH or max_width < MIN_CNN_WIDTH:
		return None

	kernel_height = np.random.randint(MIN_CNN_WIDTH, max_height+1)
	kernel_width = np.random.randint(MIN_CNN_WIDTH, max_width+1)

	# The stride can be up to
	# ((input_size - kernel_size + 1) / min_output_size) + 1
	max_stride_height = ((input_height - kernel_height + 1) / min_output_height) + 1
	max_stride_width = ((input_width - kernel_width + 1) / min_output_width) + 1

	max_stride_height = min(MAX_CNN_STRIDE, max_stride_height)
	max_stride_width = min(MAX_CNN_STRIDE, max_stride_width)

	# Stride cannot exced kernel size
	max_stride_height = min(max_stride_height, kernel_height)
	max_stride_width = min(max_stride_width, kernel_width)

	if max_stride_height < MIN_CNN_STRIDE or max_stride_width < MIN_CNN_STRIDE:
		return None

	conv_stride_height = np.random.randint(MIN_CNN_STRIDE, max_stride_height+1)
	conv_stride_width = np.random.randint(MIN_CNN_STRIDE, max_stride_width+1)

	num_kernels = np.random.randint(MIN_CNN_KERNELS, MAX_CNN_KERNELS+1)

	# activation_function ???
	return Conv2DGene((kernel_height, kernel_width), (conv_stride_height, conv_stride_width), num_kernels, activation_function=None)

"""
# Helper function
# randomly generate a PoolGene based on the lastGene's output dimension
"""
def generate1DPoolGene(lastGene, nextGene):
	## specify the min and max for each random functions
	input_size = lastGene.outputDimension()[0]
	min_output_size = nextGene.minInputDimension()[0]

	# The largest the pooling size can be is
	# input_size - min_output_size + 1
	max_size = min(MAX_POOL_SIZE, input_size - min_output_size + 1)
	if max_size < MIN_POOL_SIZE:
		return None

	pool_size = np.random.randint(MIN_POOL_SIZE, max_size+1)

	# The largest the strice can be is
	# ((input_size - pool_size + 1) / min_output_size) + 1
	max_stride = ((input_size - pool_size + 1) / min_output_size) + 1

	# Stride cannot exceed pool size
	max_stride = min(max_stride, pool_size)
	max_stride = min(max_stride, MAX_POOL_STRIDE)

	if max_strice < MIN_POOL_STRIDE:
		return None

	pool_stride = np.random.randint(MIN_POOL_STRIDE, max_stride + 1)

	# activation_function ???
	return Pool1DGene((pool_size,), (pool_stride,))


def generate2DPoolGene(lastGene, nextGene):

	input_height, input_width, _ = lastGene.outputDimension()
	min_output_size = nextGene.minInputDimension()

	min_output_height = 1
	min_output_width = 1

	if len(min_output_size) > 1:
		min_output_height = min_output_size[0]
		min_output_width = min_output_size[1]

	min_height = MIN_POOL_SIZE
	min_width = MIN_POOL_SIZE

	## specify the min and max for each random functions
	max_height = min(MAX_POOL_SIZE, input_height - min_output_height + 1)
	max_width = min(MAX_POOL_SIZE, input_width - min_output_width + 1)

	if max_height < min_height or max_width < min_width:
		return None

	pool_height = np.random.randint(min_height, max_height+1)
	pool_width = np.random.randint(min_width, max_width+1)

	# Determine maximimum stride
	max_stride_height = ((input_height - pool_height + 1) / min_output_height) + 1
	max_stride_width = ((input_width - pool_width + 1) / min_output_width) + 1

	max_stride_height = min(max_stride_height, pool_height)
	max_stride_height = min(max_stride_height, MAX_POOL_STRIDE)
	max_stride_width = min(max_stride_width, pool_width)
	max_stride_width = min(max_stride_width, MAX_POOL_STRIDE)

	if max_stride_height < MIN_POOL_STRIDE or max_stride_width < MIN_POOL_STRIDE:
		return None

	pool_stride_height = np.random.randint(MIN_POOL_STRIDE, max_stride_height + 1)
	pool_stride_width = np.random.randint(MIN_POOL_STRIDE, max_stride_width + 1)

	# activation_function ???
	return Pool2DGene((pool_height, pool_width), (pool_stride_height, pool_stride_width))



###########################################################################
###########################################################################


class CNN_Individual(AbstractIndividual):
	"""
	An individual encoding a CNN
	"""

	def __init__(self, input_shape, output_size, evaluator, mutation_rate = 0.25):
		"""
		"""

		AbstractIndividual.__init__(self)

		# Probabilities of generating convolution, pooling and fully connected layers
		self.convolutionProb = 0.5
		self.poolingProb = 0.5
		self.fullConnectionProb = 0.5

		self.input_shape = input_shape
		self.output_size = output_size

		# Is this a 1D or 2D CNN?
		if len(input_shape) == 3:
			self.is2D = True
			self.__generateConvGene = generate2DConvGene
			self.__generatePoolGene = generate2DPoolGene
		elif len(input_shape) == 2:
			self.is2D = False
			self.__generateConvGene = generate1DConvGene
			self.__generatePoolGene = generate1DPoolGene
		else:
			# Not a valid input shape (yet?)
			print "Invalid input dimensionality: %d" % len(input_shape)

		# Create a genotype
		self.genotype = self.generateGenotype()
#		self.gene = Genotype(input_shape, output_size)

		self.objective = [100000.0, 100000.0]

		self.mutation_rate = mutation_rate

		self.evaluator = evaluator


	def calculateObjective(self):
		"""
		"""

		self.evaluator.add(self)


	def link_genes(self):
		"""
		Connect the individual genes in the genotype
		"""

		for i in range(len(self.genotypee) - 1):
			self.genotype[i].next_gene = self.genotype[i+1]
			self.genotype[i+1].prev_gene = self.genotype[i]


	def __generateFullConnection(self, lastGene, nextGene=None):
		## specify the min and max for each random functions
		size = np.random.randint(MIN_FULL_CONNECTION, MAX_FULL_CONNECTION+1)

		# activation_function ???
		return FullyConnectedGene(size, activation_function=None)


	def clone(self):
		"""
		Make a copy of me!
		"""

		clone = CNN_Individual(self.input_shape, self.output_shape, self.evaluator)
		#clone.gene = self.gene.clone()
		clone.genotype = [gene.clone() for gene in self.genotype]
		clone.link_genes()
		clone.objective = [o for o in self.objective]

		return clone


	def isEqual(self, other):
		"""
		Check if 'I' have the same genotype as 'other' does
		"""

		if len(self.genotype) == len(other.genotype):
			for i in range(len(self.genotype)):
				if str(self.genotype[i]) != str(other.genotype[i]):
					return False
			return True
		else:
			return False


	def crossover(self, other):
		"""
		Perform crossover between these two individuals
		"""

		child1 = self.clone()
		child2 = other.clone()

		# Neither children have been evaluated...

		child1.objective = [100000.0, 100000.0]
		child2.objective = [100000.0, 100000.0]

		# What are valid crossover points?
		crossover_points = []

		for i, j in zip(range(1, len(child1.genotype)), range(1, len(child2.genotype))):
			if child1.genotype[i].canFollow(child2.genotype[j-1]) and child2.genotype[j].canFollow(child1.genotype[i-1]):
				# Are we just swapping inputs or outputs?
				if i==1 and j==1:
					pass
				elif i==len(child1.genotype) and j==len(child2.genotype):
					pass
				else:
					crossover_points.append((i,j))

		# if the list is empty, cannot crossover---force a mutation instead
		if len(crossover_points) == 0:
			child1.mutate()
			child2.mutate()

		else:
			# Make two new genotypes
			crossover_point = random.choice(crossover_points)

			child_gene1 = []
			child_gene2 = []

			# Populate the first half of each children
			for i in range(crossover_point[0]):
				child_gene1.append(child1.genotype[i])
			for j in range(crossover_point[1]):
				child_gene2.append(child2.genotype[j])

			# Populate the second half of each child
			for i in range(crossover_point[0], len(child1.genotype)):
				child_gene2.append(child1.genotype[i])
			for j in range(crossover_point[1], len(child2.genotype)):
				child_gene1.append(child2.genotype[j])

			child1.genotype = child_gene1
			child2.genotype = child_gene2

			# Link the previous and next genes in each child
			child1.link_genes()
			child2.link_genes()

		return child1, child2


	def mutate(self):
		"""
		Mutate this individual
		"""

		# The NSGA-II algorithm automatically calls mutate.  Would like to
		# have mutation actually be a rare occurance, due to crossover

		"""
		Mutate this individual
		"""

		added = False
		removed = False
		mutated = False


		# Should a layer be removed?
		if np.random.random() < MUTATE_REMOVE_PROB:

			print "Try to remove gene;",

			# Shuffle the indices of the genotype, and try to remove a layer until successful
			idx = range(len(self.genotype))
			idx = np.random.permutation(idx)

			i = 0

			while not removed and i < len(idx):
				# Cannot remove the input or output layer
				if self.genotype[idx[i]].type == INPUT or self.genotype[idx[i]].type == OUTPUT:
					i += 1
				# Can't remove a layer which would put two pooling layers next to each other
				elif self.genotype[idx[i]-1].type == POOL1D and self.genotype[idx[i]+1].type == POOL1D:
					i += 1
				elif self.genotype[idx[i]-1].type == POOL2D and self.genotype[idx[i]+1].type == POOL2D:
					i += 1
				else:
					# Go ahead and remove this!
					self.genotype = self.genotype[:idx[i]] + self.genotype[idx[i]+1:]
					removed = True
					print "Removed Gene;",

			# Clean up the genotype
			self.link_genes()


		# Should a layer be added?
		if np.random.random() < MUTATE_ADD_PROB:

			print "Try to add gene;",
			"""
			ISSUE:  Adding a 2D Convolutional layer sometimes generates incorrect layers (i.e., kernel size bigger than input...)
			"""
			# Right now, should be able to add after any layer
			idx = np.random.randint(0,len(self.genotype) - 1)

			# Available layers
			layer_types = []

			# Can add a convolutional layer if the previous layer is input, convolutional or pooling
			if self.genotype[idx].type in [INPUT, CONV1D, CONV2D, POOL1D, POOL2D]:
				layer_types.append('conv')

			# Can add a pooling lyaer if the previous layer is input or convolutional, and if
			# the next layer isn't a pooling layer
			if self.genotype[idx].type in [INPUT, CONV1D, CONV2D] and not self.genotype[idx+1].type in [POOL1D,POOL2D]:
				layer_types.append('pool')

			# Can add a fully connected layer if the next layer is fully connected or output
			if self.genotype[idx].type in [FULLY_CONNECTED, OUTPUT]:
				layer_types.append('fc')

			# Pick a layer type
			layer_type = np.random.choice(layer_types)

			if layer_type == 'conv':
				layer = self.__generateConvGene(self.genotype[idx], self.genotype[idx+1])
			elif layer_type == 'pool':
				layer = self.__generatePoolGene(self.genotype[idx], self.genotype[idx+1])
			elif layer_type == 'fc':
				layer = self.__generateFullConnection(self.genotype[idx])

			if layer:
				# Sanity check--is the output dimensionality negative for any element from this layer?
				dummy_input = DummyGene(self.genotype[idx].outputDimension())
				layer.prev_gene = dummy_input
				layer_output_size = layer.outputDimension()

				if layer_type == 'fc':
					layer_output_size = (layer_output_size,)

				is_valid = True
				for d in layer_output_size:
					if d < 1:
						is_valid = False

				if not is_valid:
					print "Gene not added - negative dimension output:", layer_type, ";"
					added = False
				else:
					self.genotype = self.genotype[:idx+1] + [layer] + self.genotype[idx+1:]
					self.link_genes()

					# Clean up the genotype
					added = True
					print "Added Gene;",
			else:
				print "Gene not added - unable to create: ", layer_type, ";"


		if np.random.random() < MUTATE_MODIFY_PROB:

			print "Trying to mutate gene;",

			# Shuffle the indices of the genotype, and perform mutation on the items in the list until sucessful
			idx = range(len(self.genotype))
			idx = np.random.permutation(idx)

			i = 0

			while not mutated and i < len(idx):
				mutated = self.genotype[idx[i]].mutate()
				i += 1

			if mutated:
				print "Mutated Gene;",

			self.link_genes()

		# Inform if the genotype has actually changed
		if not (mutated or added or removed):
			print "Did not mutate!"
		else:
			print

		return mutated or added or removed


	def generateGenotype(self):
		"""
		Create the actual genotype
		"""

		lastGene = InputGene(self.input_shape)
		outGene = OutputGene(self.output_size)

		lastGene.next_gene = outGene

		genotype = [lastGene]

		# Add the Convolutional Layers (and pooling layers)
		while random.random() < self.convolutionProb:
			if MIN_CNN_WIDTH > lastGene.outputDimension()[0]:
				break
			if self.is2D and MIN_CNN_WIDTH > lastGene.outputDimension()[1]:
				break

			# Add the convolution layer, with random genes
			tempGene = self.__generateConvGene(lastGene, outGene)
			tempGene.next_gene = outGene

			if tempGene.canFollow(lastGene):
				lastGene.next_gene = tempGene
				tempGene.prev_gene = lastGene
				lastGene = tempGene
				genotype.append(lastGene)
			else:
				# Failed to create a genotype
				return None

			# Should this be followed by a pooling layer?
			if random.random() < self.poolingProb:
				if MIN_POOL_SIZE > lastGene.outputDimension()[0]:
					break
				if self.is2D and MIN_POOL_SIZE > lastGene.outputDimension()[1]:
					break

				tempGene = self.__generatePoolGene(lastGene, outGene)
				tempGene.next_gene = outGene

				if tempGene.canFollow(lastGene):
					lastGene.next_gene = tempGene
					tempGene.prev_gene = lastGene
					lastGene = tempGene
					genotype.append(lastGene)

				else:
					# Failed to create a genotype
					return None

		# Fill in fully connected layers
		while random.random() < self.fullConnectionProb:
			tempGene = self.__generateFullConnection(lastGene)
			tempGene.next_gene = outGene

			if tempGene.canFollow(lastGene):
				lastGene.next_gene = tempGene
				tempGene.prev_gene = lastGene
				lastGene = tempGene
				genotype.append(lastGene)

			else:
				# Failed to create a genotype
				return None

		# Genotype successfully created
		outGene.prev_gene = genotype[-1]
		genotype.append(outGene)

		return genotype


	def generate_model(self, input_tensor):
		"""
		Build the tensorflow model
		"""

		if input_tensor == None:
			print "ARGH!"
			print self
			print
			return None

		prev_tensor = input_tensor

		tensors = []

		for gene in self.genotype:
			prev_tensor = gene.generateLayer(prev_tensor)
			if prev_tensor == None:
				print "AAARG!"
				print gene
				print
			tensors.append(prev_tensor)

		# Return the input and output tensor
		return tensors[0], tensors[-1]


	def __str__(self):
		"""
		Provide a representation of this individual
		"""

		string = ""

		for gene in self.genotype[:-1]:
			string += str(gene) + '\n'
		string += str(self.genotype[-1])

		return string