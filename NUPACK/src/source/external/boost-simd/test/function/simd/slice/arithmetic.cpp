//==================================================================================================
/*!

  Copyright 2016 NumScale SAS

  Distributed under the Boost Software License, Version 1.0.
  (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)
*/
//==================================================================================================
#include <boost/simd/function/slice.hpp>
#include <boost/simd/pack.hpp>
#include <simd_test.hpp>

namespace bs = boost::simd;


template<typename T, std::size_t N, typename Env>
void test( Env&, brigand::bool_<false> const& )
{}

template<typename T, std::size_t N, typename Env>
void test( Env& $, brigand::bool_<true> const& = {} )
{
  std::array<T,N> ref;
  for(std::size_t i=0;i<N;++i) ref[i] = T(1+i);

  bs::pack<T,N>   value (&ref[0]  , &ref[0]+N   );
  bs::pack<T,N/2> first (&ref[0]  , &ref[0]+N/2 );
  bs::pack<T,N/2> second(&ref[0]+N/2, &ref[0]+N );

  auto sliced = bs::slice(value);

  STF_EQUAL( sliced[0], first);
  STF_EQUAL( sliced[1], second);
}

STF_CASE_TPL("slice pack<T,N> into 2 pack<T,N/2>", STF_NUMERIC_TYPES)
{
  static const std::size_t N = bs::pack<T>::static_size;

  test<T,N>($);
  test<T,N/2>($, brigand::bool_<(N/2 > 1)>{});
  test<T,N*2>($);
}
