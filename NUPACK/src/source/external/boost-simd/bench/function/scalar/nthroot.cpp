// -------------------------------------------------------------------------------------------------
//                              Copyright 2016 - NumScale SAS
//
//                   Distributed under the Boost Software License, Version 1.0.
//                        See accompanying file LICENSE.txt or copy at
//                            http://www.boost.org/LICENSE_1_0.txt
// -------------------------------------------------------------------------------------------------

#include <simd_bench.hpp>
#include <boost/simd/function/simd/nthroot.hpp>
#include <boost/simd/function/simd/enumerate.hpp>
#include <cmath>
#include <boost/simd/detail/dispatch/meta/as_integer.hpp>

namespace nsb = ns::bench;
namespace bs =  boost::simd;
namespace bd =  boost::dispatch;

struct nthr
{
  template<class T> T operator()(const T & a) const
  {
    using i_t = bd::as_integer_t<T>;
    return bs::nthroot(a, bs::enumerate<i_t>(2));
  }
};

struct nthrf
{
  template<class T> T operator()(const T & a) const
  {
    using i_t = bd::as_integer_t<T>;
    return bs::fast_(bs::nthroot)(a, bs::enumerate<i_t>(2));
  }
};

DEFINE_SCALAR_BENCH(scalar_nthroot, nthr());
DEFINE_SCALAR_BENCH(fast_scalar_nthroot, nthrf());

DEFINE_BENCH_MAIN() {
  nsb::for_each<scalar_nthroot, NS_BENCH_IEEE_TYPES>(-10, 10);
  nsb::for_each<fast_scalar_nthroot, NS_BENCH_IEEE_TYPES>(-10, 10);
}


