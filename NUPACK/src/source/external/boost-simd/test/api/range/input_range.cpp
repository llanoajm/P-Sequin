//==================================================================================================
/**
  Copyright 2016 NumScale SAS

  Distributed under the Boost Software License, Version 1.0.
  (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)
**/
//==================================================================================================
#include <boost/simd/range/input_range.hpp>
#include <boost/simd/pack.hpp>
#include <boost/simd/memory/allocator.hpp>
#include <boost/range.hpp>
#include <simd_test.hpp>
#include <vector>

template<typename Range, typename Out> inline void mycopy(Range const& r, Out dst)
{
  for( auto const& p : r)  *dst++ = p;
}

STF_CASE_TPL("distance", STF_NUMERIC_TYPES)
{
  using boost::simd::input_range;
  using boost::simd::pack;

  std::vector<T> data(pack<T>::static_size*3), data2(24);

  auto rng  = input_range(data);
  auto rng8 = input_range<8>(data2);

  STF_EQUAL( std::distance(std::begin(rng) , std::end(rng) ), 3 );
  STF_EQUAL( std::distance(std::begin(rng8), std::end(rng8)), 3 );
}

STF_CASE_TPL("iteration", STF_NUMERIC_TYPES)
{
  using boost::simd::input_range;
  using boost::simd::pack;

  std::vector<pack<T>,boost::simd::allocator<T>>  dst(3), ref(3);
  std::vector<T>          data(pack<T>::static_size*3);

  for(std::size_t i=0;i<data.size();i++)
    data[i] = i/pack<T>::static_size+1;

  for(std::size_t i=0;i<ref.size();i++)
    ref[i] = pack<T>(i+1);

  auto simd_range = input_range(data);
  mycopy(simd_range , dst.begin());

  STF_ALL_EQUAL( ref, dst );
}
