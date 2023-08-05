/*
 * Open Chinese Convert
 *
 * Copyright 2010-2014 Carbo Kuo <byvoid@byvoid.com>
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#pragma once

#include <list>

#include "Common.hpp"
#include "Conversion.hpp"

namespace opencc {
/**
 * Chain of conversions
 * Consists of a list of conversions. Converts input in sequence.
 * @ingroup opencc_cpp_api
 */
class OPENCC_EXPORT ConversionChain {
public:
  ConversionChain(const std::list<ConversionPtr> _conversions);

  SegmentsPtr Convert(const SegmentsPtr& input) const;

  const std::list<ConversionPtr> GetConversions() const { return conversions; }

private:
  const std::list<ConversionPtr> conversions;
};
} // namespace opencc
