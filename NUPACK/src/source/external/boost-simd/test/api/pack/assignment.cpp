//==================================================================================================
/*
  Copyright 2016 NumScale SAS

  Distributed under the Boost Software License, Version 1.0.
  (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)
*/
//==================================================================================================

#include <boost/simd/pack.hpp>
#include <boost/align/aligned_alloc.hpp>
#include <numeric>
#include <simd_test.hpp>

template <typename T, std::size_t N, typename Env>
void test(Env& $)
{
  namespace ba = boost::alignment;
  using pack_t = boost::simd::pack<T, N>;

  std::array<T, N> data;
  data.fill(N); // Use the cardinal as scalar value

  pack_t p;

  p = N;
  STF_EXPECT( std::equal(p.begin(), p.end(), data.begin()) );
}

STF_CASE_TPL("Check pack assignment operator with scalar value" , STF_NUMERIC_TYPES)
{
  test<T,  2>($);
  test<T,  4>($);
  test<T,  8>($);
  test<T, 16>($);
  test<T, 32>($);
}
