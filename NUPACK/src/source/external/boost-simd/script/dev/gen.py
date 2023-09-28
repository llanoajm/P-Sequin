#!/usr/bin/env python2

#==============================================================================
#         Copyright 2016 NumScale SAS
#
#         Distributed under the Boost Software License, Version 1.0.
#                See accompanying file LICENSE.txt or copy at
#                    http://www.boost.org/LICENSE_1_0.txt
#==============================================================================

import sys, argparse, os, errno

"""
The following lists are lists of valid extensions for a given architecture
"""

x86_exts = [
        'avx',
        'avx2',
        'fma3',
        'fma4',
        'mic',
        'sse1',
        'sse2',
        'sse3',
        'sse41',
        'sse42',
        'sse4a',
        'ssse3',
        'xop',
        ]

arm_exts = [
        'neon',
        ]

ppc_exts = [
        'qpx',
        'vmx',
        'vsx',
        ]

# globals
_license = None

"""
Say something!
"""
def say(*args):
    print(':: {0}'.format(' '.join(str(a) for a in args)))
"""
Parse options. Here is the list of supported options:
    see `help`(s)
"""
def parse_opts(args):
    default_rootdir = '$BOOST_ROOT/libs/simd'

    p = argparse.ArgumentParser(
            description='Generate skeleton files for a given name')
    p.add_argument('--scalar', dest='with_scalar', action='store_true', default=False,
            help='Enable scalar skeleton generation')
    p.add_argument('--common-simd', dest='with_common_simd', action='store_true', default=False,
            help='Enable SIMD skeleton generation')
    p.add_argument('--x86', dest='with_x86', nargs='*', default=[], metavar='<ext>',
            help='Enable x86 SIMD skeleton generation')
    p.add_argument('--arm', dest='with_arm', nargs='*', default=[], metavar='<ext>',
            help='Enable ARM SIMD skeleton generation')
    p.add_argument('--ppc', dest='with_ppc', nargs='*', default=[], metavar='<ext>',
            help='Enable PowerPC SIMD skeleton generation')
    p.add_argument('--root', dest='rootdir', metavar='<root-directory>',
            help='The root directory of boost.simd (default is: {0})'.format(default_rootdir))
    p.add_argument('--nargs', type=int, default=1, metavar='<number-of-arguments>',
            help='The number of argument that takes the function')
    p.add_argument('--license-from-file', type=str, metavar='<path-to-license-header>',
            help='Read the license header from a file (do not forget c++ comments!)')
    p.add_argument('name',
            help='The function name to generate')

    opts = p.parse_args(args)

    if not opts.rootdir:
        boost_root = os.getenv('BOOST_ROOT')
        if not boost_root:
            say('$BOOST_ROOT is not defined')
            sys.exit(1)
        path = boost_root + '/libs/simd'
        if not os.path.exists(path):
            say('"{0}": no such directory'.format(path))
            sys.exit(1)
        opts.rootdir = path
    say('Using "{0}" as root directory'.format(opts.rootdir))

    for ext in opts.with_x86:
        if ext not in x86_exts:
            say('"{0}" is not a valid x86 extension, must be one of those:'.format(ext))
            say(str(x86_exts))
            sys.exit(1)

    for ext in opts.with_arm:
        if ext not in arm_exts:
            say('"{0}" is not a valid ARM extension, must be one of those:'.format(ext))
            say(str(arm_exts))
            sys.exit(1)

    for ext in opts.with_ppc:
        if ext not in ppc_exts:
            say('"{0}" is not a valid PowerPC extension, must be one of those:'.format(ext))
            say(str(ppc_exts))
            sys.exit(1)

    return opts

"""
"""
def license(opts):
    global _license
    for line in _license:
        yield line

"""
"""
def include(path):
    return '#include <{0}>'.format(path)

"""
"""
def guard(path, generator):
    path = path.split('.hpp')[0]
    pattern = '_'.join(s.upper() for s in path.split(os.path.sep))
    pattern += '_HPP_INCLUDED'
    yield '#ifndef {0}'.format(pattern)
    yield '#define {0}'.format(pattern)
    yield ''
    for line in generator:
        yield line
    yield ''
    yield '#endif'

"""
"""
def make_function(opts, hpp):
    t = '  '
    typenames = ', '.join('typename T{0}'.format(n) for n in range(0, opts.nargs))
    arguments = ', '.join('T{0} const& a{0}'.format(n) for n in range(0, opts.nargs))
    yield '#if defined(DOXYGEN_ONLY)'
    yield 'namespace boost { namespace simd'
    yield '{'
    yield t * 1 + '/*!'
    yield t * 1 + '@ingroup TODO(doc-group)'
    yield t * 1 + ''
    yield t * 1 + '**/'
    yield t * 1 + 'template <{0}>'.format(typenames)
    yield t * 1 + 'auto {0}({1}) {{}}'.format(opts.name, arguments)
    yield t * 1 + 'namespace functional'
    yield t * 1 + '{'
    yield t * 2 + '/*!'
    yield t * 2 + '@ingroup TODO(doc-group)'
    yield t * 2 + ''
    yield t * 2 + '**/'
    yield t * 2 + 'const boost::dispatch::functor<tag::{0}_> {0} = {{}};'.format(opts.name)
    yield t * 1 + '}'
    yield '} }'
    yield '#endif'
    yield ''
    yield include('boost/simd/function/definition/{0}'.format(hpp))
    yield include('boost/simd/function/scalar/{0}'.format(hpp))
    yield include('boost/simd/function/simd/{0}'.format(hpp))

"""
"""
def make_function_definition(opts):
    t = '  '
    yield include('boost/dispatch/function/make_callable.hpp')
    yield include('boost/dispatch/hierarchy/functions.hpp')
    yield include('boost/simd/detail/dispatch.hpp')
    yield ''
    yield 'namespace boost { namespace simd'
    yield '{'
    yield t * 1 + 'namespace tag'
    yield t * 1 + '{'
    yield t * 2 + 'BOOST_DISPATCH_MAKE_TAG(ext, {0}_, boost::dispatch::elementwise_<{0}_>);'.format(opts.name)
    yield t * 1 + '}'
    yield ''
    yield t * 1 + 'namespace ext'
    yield t * 1 + '{'
    yield t * 2 + 'BOOST_DISPATCH_FUNCTION_DECLARATION(tag, {0}_)'.format(opts.name)
    yield t * 1 + '}'
    yield ''
    yield t * 1 + 'namespace functional'
    yield t * 1 + '{'
    yield t * 2 + 'BOOST_DISPATCH_CALLABLE_DEFINITION(tag::{0}_, {0});'.format(opts.name)
    yield t * 1 + '}'
    yield ''
    yield t * 1 + 'BOOST_DISPATCH_FUNCTION_DEFINITION(tag::{0}_, {0});'.format(opts.name)
    yield ''
    yield '} }'

"""
"""
def make_arch_ext_function(opts, arch, ext):
    t = '  '
    typenames = ', '.join('typename T{0}'.format(n) for n in range(0, opts.nargs))
    arguments = ', '.join('T{0} const& a{0}'.format(n) for n in range(0, opts.nargs))
    unspecifieds = ', '.join('bs::unspecified_<T{0}>'.format(n) for n in range(0, opts.nargs))
    yield include('boost/config.hpp')
    yield include('boost/dispatch/function/overload.hpp')
    yield ''
    yield 'namespace boost { namespace simd { namespace ext'
    yield '{'
    yield t * 1 + 'namespace bd = boost::dispatch;'
    yield ''
    yield t * 1 + '// TODO({0}-{1}-function)'.format(arch, ext)
    yield t * 1 + 'BOOST_DISPATCH_OVERLOAD ( {0}_'.format(opts.name)
    yield t * 1 + '                        , ({0})'.format(typenames)
    yield t * 1 + '                        , bd::{0}_'.format(ext)
    yield t * 1 + '                        , {0}'.format(unspecifieds)
    yield t * 1 + '                        )'
    yield t * 1 + '{'
    yield t * 1 + '  BOOST_FORCEINLINE auto operator()({0}) const BOOST_NOEXCEPT'.format(arguments)
    yield t * 1 + '  {'
    yield t * 1 + '  }'
    yield t * 1 + '};'
    yield ''
    yield '}'
    yield '} }'

"""
`mkdir -p` python style
"""
def make_path(path):
    if path.endswith('hpp'):
        path = os.path.dirname(path)
    try:
        say('Creating directory "{0}"'.format(path))
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise e

"""
Generate the file!
"""
def make_file(opts, path, generator, overwrite=False):
    real_path = os.path.join(opts.rootdir, 'include', path)
    if not overwrite and os.path.exists(real_path):
        say('Skipping \t"{0}"'.format(path))
        return
    say('Generating \t"{0}"...'.format(path))
    real_dir = os.path.dirname(real_path)
    if not os.path.isdir(real_dir):
        make_path(real_dir)
    try:
        with open(real_path, 'w+') as outs:
            generators = [license(opts), guard(path, generator)]
            for generator in generators:
                for line in generator:
                    outs.write(line + '\n')
        say('"{0}" generated!'.format(path))
    except IOError as e:
        say('ERROR: {0}'.format(str(e)))
        say('Skipping \t"{0}" (because of errors...)'.format(path))

"""
Generate file content for `boost/simd/function/<kind>/<name>.hpp`
"""
def make_aggregated_include(opts, hpp, exts):
    rootdir = os.path.join(opts.rootdir, 'include')
    yield include('boost/simd/function/definition/{0}'.format(hpp))
    for arch, ext in exts:
        path = os.path.join('boost/simd/arch/{0}/{1}/function/{2}'.format(arch, ext, hpp))
        real_path = os.path.join(rootdir, path)
        if os.path.exists(real_path):
            say('Aggregate "{0}"'.format(path))
            yield include(path)

"""
Generate file for `boost/simd/function/{scalar,simd}/<name>.hpp`
"""
def make_aggregated_includes(opts, hpp):
    # -- scalar
    say('# --')
    say('Aggregating \t"boost/simd/function/scalar/{0}"'.format(hpp))
    exts = [('common', 'scalar')]
    make_file(opts, 'boost/simd/function/scalar/{0}'.format(hpp), make_aggregated_include(opts, hpp, exts), overwrite=True)
    # -- simd
    say('# --')
    say('Aggregating \t"boost/simd/function/simd/{0}"'.format(hpp))
    exts = []
    exts.append(('common', 'simd'))
    for ext in x86_exts:
        exts.append(('x86', ext))
    for ext in arm_exts:
        exts.append(('arm', ext))
    for ext in ppc_exts:
        exts.append(('power', ext))
    make_file(opts, 'boost/simd/function/simd/{0}'.format(hpp), make_aggregated_include(opts, hpp, exts), overwrite=True)

"""
Initialize the license header
"""
def init_license(opts):
    global _license
    if opts.license_from_file:
        try:
            with open(opts.license_from_file, 'r') as f:
                _license = f.readlines()
        except IOError as e:
            say('Something went wrong with the license...')
            say(str(e))
            sys.exit(1)
    else:
        # The default license
        _license = [
            '//==================================================================================================',
            '/*!',
            '  @file TODO(doc-file)',
            '',
            '  @copyright 2016 NumScale SAS',
            '',
            '  Distributed under the Boost Software License Version 1.0.',
            '  (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)',
            '*/',
            '//==================================================================================================',
            ]

"""
The entry point!
"""
def gen():
    opts = parse_opts(sys.argv[1:])
    hpp = opts.name + '.hpp'
    exts = []
    if opts.with_scalar:
        exts.append(('common', 'scalar'))
    if opts.with_common_simd:
        exts.append(('common', 'simd'))
    for ext in opts.with_x86:
        exts.append(('x86', ext))
    for ext in opts.with_arm:
        exts.append(('arm', ext))
    for ext in opts.with_ppc:
        exts.append(('power', ext))
    # --
    init_license(opts)
    # --
    make_file(opts, 'boost/simd/function/{0}'.format(hpp), make_function(opts, hpp))
    make_file(opts, 'boost/simd/function/definition/{0}'.format(hpp), make_function_definition(opts))
    for arch, ext in exts:
        make_file(opts, 'boost/simd/arch/{0}/{1}/function/{2}'.format(arch, ext, hpp), make_arch_ext_function(opts, arch, ext))
    make_aggregated_includes(opts, hpp)

if __name__ == '__main__':
    gen()
