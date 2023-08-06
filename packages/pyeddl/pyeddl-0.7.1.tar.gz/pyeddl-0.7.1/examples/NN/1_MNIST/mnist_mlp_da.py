# Copyright (c) 2019-2020, CRS4
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""\
Basic MLP for MNIST with data augmentation.
"""

import argparse
import sys

import pyeddl.eddl as eddl
import pyeddl.eddlT as eddlT


def main(args):
    eddl.download_mnist()

    num_classes = 10

    in_ = eddl.Input([784])

    layer = in_
    layer = eddl.Reshape(layer, [1, 28, 28])
    layer = eddl.RandomCropScale(layer, [0.9, 1.0])
    layer = eddl.Reshape(layer, [-1])
    layer = eddl.ReLu(eddl.GaussianNoise(
        eddl.BatchNormalization(eddl.Dense(layer, 1024)), 0.3
    ))
    layer = eddl.ReLu(eddl.GaussianNoise(
        eddl.BatchNormalization(eddl.Dense(layer, 1024)), 0.3
    ))
    layer = eddl.ReLu(eddl.GaussianNoise(
        eddl.BatchNormalization(eddl.Dense(layer, 1024)), 0.3
    ))
    out = eddl.Activation(eddl.Dense(layer, num_classes), "softmax")
    net = eddl.Model([in_], [out])

    eddl.build(
        net,
        eddl.sgd(0.01, 0.9),
        ["soft_cross_entropy"],
        ["categorical_accuracy"],
        eddl.CS_GPU() if args.gpu else eddl.CS_CPU()
    )

    eddl.summary(net)
    eddl.plot(net, "model.pdf")

    x_train = eddlT.load("trX.bin")
    y_train = eddlT.load("trY.bin")
    x_test = eddlT.load("tsX.bin")
    y_test = eddlT.load("tsY.bin")

    eddlT.div_(x_train, 255.0)
    eddlT.div_(x_test, 255.0)

    eddl.fit(net, [x_train], [y_train], args.batch_size, args.epochs)
    eddl.evaluate(net, [x_test], [y_test])

    # LR annealing
    if args.epochs < 4:
        return
    eddl.setlr(net, [0.005, 0.9])
    eddl.fit(net, [x_train], [y_train], args.batch_size, args.epochs // 2)
    eddl.evaluate(net, [x_test], [y_test])
    eddl.setlr(net, [0.001, 0.9])
    eddl.fit(net, [x_train], [y_train], args.batch_size, args.epochs // 2)
    eddl.evaluate(net, [x_test], [y_test])
    eddl.setlr(net, [0.0001, 0.9])
    eddl.fit(net, [x_train], [y_train], args.batch_size, args.epochs // 4)
    eddl.evaluate(net, [x_test], [y_test])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epochs", type=int, metavar="INT", default=10)
    parser.add_argument("--batch-size", type=int, metavar="INT", default=1000)
    parser.add_argument("--gpu", action="store_true")
    main(parser.parse_args(sys.argv[1:]))
