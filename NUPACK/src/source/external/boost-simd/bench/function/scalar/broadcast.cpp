// -------------------------------------------------------------------------------------------------
//                              Copyright 2016 - NumScale SAS
//
//                   Distributed under the Boost Software License, Version 1.0.
//                        See accompanying file LICENSE.txt or copy at
//                            http://www.boost.org/LICENSE_1_0.txt
// -------------------------------------------------------------------------------------------------

#include <simd_bench.hpp>
#include <boost/simd/function/simd/broadcast.hpp>

namespace nsb = ns::bench;
namespace bs =  boost::simd;
struct broad
{
  template<class T> T operator()(const T & a) const
  {
    return bs::broadcast<1>(a);
  }
};

DEFINE_SCALAR_BENCH(scalar_broadcast, broad());

DEFINE_BENCH_MAIN() {
  nsb::for_each<scalar_broadcast, NS_BENCH_NUMERIC_TYPES>(-10, 10);
}

