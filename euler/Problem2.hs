module Problem2
where

import System.Time


fibs :: [Integer]
fibs = 1 : 2 : zipWith (+) fibs (tail fibs)

