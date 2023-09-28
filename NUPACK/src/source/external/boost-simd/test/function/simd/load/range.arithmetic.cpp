//==================================================================================================
/*!

  Copyright 2016 NumScale SAS

  Distributed under the Boost Software License, Version 1.0.
  (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)
*/
//==================================================================================================
#include <boost/simd/function/simd/load.hpp>
#include <boost/simd/pack.hpp>
#include <simd_test.hpp>
#include <vector>
#include <list>

template <typename T, std::size_t N, typename Container, typename Env>
void test(Env& $)
{
  namespace bs = boost::simd;
  using p_t = bs::pack<T,N>;

  Container c;
  for(std::size_t i=0;i<N;++i) c.push_back(T(i+1));

  p_t p;
  p = bs::load<p_t>(c.begin(),c.end());

  STF_ALL_EQUAL( p, c );
}

STF_CASE_TPL( "Check load behavior with InputRange", STF_NUMERIC_TYPES )
{
  namespace bs = boost::simd;
  static const std::size_t N = bs::pack<T>::static_size;

  test<T, N  , std::list<T>>($);
  test<T, N/2, std::list<T>>($);
  test<T, N*2, std::list<T>>($);
}

STF_CASE_TPL( "Check load behavior with RandomAccessRange", STF_NUMERIC_TYPES )
{
  namespace bs = boost::simd;
  static const std::size_t N = bs::pack<T>::static_size;

  test<T, N  , std::vector<T>>($);
  test<T, N/2, std::vector<T>>($);
  test<T, N*2, std::vector<T>>($);
}
