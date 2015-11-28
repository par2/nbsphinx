# Copyright (c) 2015 Matthias Geier
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Sphinx source parser for ipynb files."""
__version__ = '0.0.0'

import docutils
import nbconvert
import nbformat
import os

_ipynbversion = 4


class NotebookParser(docutils.parsers.rst.Parser):

    def parse(self, inputstring, document):
        nb = nbformat.reads(inputstring, as_version=_ipynbversion)

        env = document.settings.env

        resources = {}

        # Execute notebook only if there are no outputs:
        if not any(c.outputs for c in nb.cells if 'outputs' in c):
            dirname = os.path.dirname(env.doc2path(env.docname))
            resources.setdefault('metadata', {})['path'] = dirname
            pp = nbconvert.preprocessors.ExecutePreprocessor()
            nb, resources = pp.preprocess(nb, resources)

        # TODO: save a copy of the notebook with and without outputs
        #       (see document.get('source'))

        exporter = nbconvert.RSTExporter()
        rststring, resources = exporter.from_notebook_node(nb, resources)

        docutils.parsers.rst.Parser.parse(self, rststring, document)