# This file is part of Marcel.
# 
# Marcel is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or at your
# option) any later version.
# 
# Marcel is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Marcel.  If not, see <https://www.gnu.org/licenses/>.

import marcel.argsparser
import marcel.core
import marcel.exception
import marcel.opmodule
import marcel.object.error
import marcel.util

SUMMARY = '''
Computes a database-style join between the incoming stream, 
and the input stream from a second pipeline.
'''

DETAILS = '''
The input pipeline provides one input to the join, named {i:left}.
The {r:pipeline} argument provides the second input, named {i:right}.
Left and right tuples are matched by comparing the first component. For matching
pairs, an output tuple consists of the left input followed by the right row with the
first value removed. (That would be redundant since the tuples were matched on their
first values.)

The {r:--keep} flag causes left inputs to be passed to output as is, when there is no
matching right input. (In database terms, this is a left join.)

{b:Example}

The left input has 6 tuples of the form {n:(x, -x)}, generated by {n:gen 6 | map (x: (x, -x))}.
The right input has 4 tuples of the form {n:(x, x**2)}, generated by {n:gen 4 | map (x: (x, x**2))}.
The join is computed as follows:

{L,wrap=F}gen 6 | map (x: (x, -x)) | join [ gen 4 | map (x: (x, x**2)) ]

This generates the following output:

{L,wrap=F,indent=4}
(0, 0, 0)
(1, -1, 1)
(2, -2, 4)
(3, -3, 9)

If the {r:--keep} flag were included, the output would have two additional rows:

{L,wrap=F,indent=4}
(0, 0, 0)
(1, -1, 1)
(2, -2, 4)
(3, -3, 9)
(4, -4)
(5, -5)
'''


def join(env, pipeline, keep=False):
    assert isinstance(pipeline, marcel.core.Pipelineable)
    args = ['--keep'] if keep else []
    args.append(pipeline.create_pipeline())
    return Join(env), args


class JoinArgsParser(marcel.argsparser.ArgsParser):

    def __init__(self, env):
        super().__init__('join', env)
        self.add_flag_no_value('keep', '-k', '--keep')
        # str: To accommodate var names
        self.add_anon('pipeline', convert=self.check_str_or_pipeline)
        self.validate()

    def check_str_or_pipeline(self, arg, x):
        if type(x) not in (str, marcel.core.Pipeline):
            raise marcel.argsparser.ArgsError(self.op_name,
                                              f'{arg.name} argument must be a Pipeline: {x}')
        return x


class Join(marcel.core.Op):

    def __init__(self, env):
        super().__init__(env)
        self.pipeline = None
        self.keep = None
        self.pipeline_map = None  # Map containing contents of pipeline, keyed by join value

    def __repr__(self):
        return 'join(keep)' if self.keep else 'join()'

    # BaseOp

    def setup_1(self):
        def load_pipeline_map(*x):
            join_value = x[0]
            match = self.pipeline_map.get(join_value, None)
            if match is None:
                self.pipeline_map[join_value] = x
            elif type(match) is list:
                match.append(x)
            else:
                # match is first value associated with join_value, x is the second. Need a list.
                self.pipeline_map[join_value] = [match, x]
        self.pipeline_map = {}
        # self.pipeline is permitted to be one of:
        #     - a pipeline literal: [ ... ]
        #     - a var bound to a pipeline
        #     - TODO: an expression that evaluates to a pipeline, e.g. (pipeline_var)
        if isinstance(self.pipeline, marcel.core.Pipelineable):
            pipeline = self.pipeline.create_pipeline()
        else:
            pipeline = self.env().getvar(self.pipeline)
        if type(pipeline) is not marcel.core.Pipeline:
            raise marcel.exception.KillCommandException(f'The variable {self.pipeline} is not bound to a pipeline')
        pipeline = pipeline.copy()
        pipeline.set_error_handler(self.owner.error_handler)
        pipeline.append(marcel.opmodule.create_op(self.env(), 'map', load_pipeline_map))
        marcel.core.Command(None, pipeline).execute()

    def receive(self, x):
        join_value = x[0]
        match = self.pipeline_map.get(join_value, None)
        if match is None:
            if self.keep:
                self.send(x)
        elif type(match) is list:
            for m in match:
                self.send(x + m[1:])
        else:
            self.send(x + match[1:])
