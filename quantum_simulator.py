import logging
import math
import random

logger = logging.getLogger(__name__)


def gcd(a, b):
    logger.debug("gcd called with a=%d, b=%d", a, b)
    while b:
        a, b = b, a % b
    return a


def mod_pow(base, exponent, modulus):
    logger.debug("mod_pow called with base=%d, exponent=%d, modulus=%d", base, exponent, modulus)
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result


def find_period(a, n):
    logger.debug("find_period called with a=%d, n=%d", a, n)
    r = 1
    while mod_pow(a, r, n) != 1:
        r += 1
        if r > n:
            logger.warning("Period not found for a=%d, n=%d", a, n)
            return None
    logger.info("Found period r=%d for a=%d mod %d", r, a, n)
    return r


def shor_factor(n, max_attempts=100):
    logger.debug("shor_factor called with n=%d", n)

    if n < 2:
        logger.warning("n=%d is less than 2", n)
        return None

    if n % 2 == 0:
        logger.info("n=%d is even, trivial factor is 2", n)
        return 2

    for k in range(2, int(math.log2(n)) + 1):
        root = round(n ** (1.0 / k))
        for candidate in [root - 1, root, root + 1]:
            if candidate > 1 and candidate ** k == n:
                logger.info("n=%d is a perfect power: %d^%d", n, candidate, k)
                return candidate

    for attempt in range(max_attempts):
        a = random.randint(2, n - 1)
        logger.debug("Attempt %d: trying a=%d", attempt + 1, a)

        d = gcd(a, n)
        if d > 1:
            logger.info("Found factor %d by gcd on attempt %d", d, attempt + 1)
            return d

        r = find_period(a, n)
        if r is None or r % 2 != 0:
            continue

        x = mod_pow(a, r // 2, n)
        if x == n - 1:
            continue

        factor1 = gcd(x - 1, n)
        factor2 = gcd(x + 1, n)

        if 1 < factor1 < n:
            logger.info("Found factor %d on attempt %d", factor1, attempt + 1)
            return factor1
        if 1 < factor2 < n:
            logger.info("Found factor %d on attempt %d", factor2, attempt + 1)
            return factor2

    logger.warning("Failed to factor %d after %d attempts", n, max_attempts)
    return None


def simulate_quantum_factoring(n, num_qubits=None):
    logger.debug("simulate_quantum_factoring called with n=%d, num_qubits=%s", n, num_qubits)

    if num_qubits is None:
        num_qubits = max(2 * math.ceil(math.log2(n + 1)), 4)

    if num_qubits > 1000:
        logger.warning("num_qubits=%d exceeds maximum of 1000", num_qubits)
        return {"success": False, "error": "num_qubits exceeds maximum of 1000"}

    if n < 2:
        return {"success": False, "error": "n must be >= 2"}

    if is_prime(n):
        return {"success": False, "error": f"{n} is prime"}

    factor = shor_factor(n)
    if factor is None:
        return {"success": False, "error": f"Failed to factor {n}"}

    other = n // factor
    logger.info("Factored %d = %d x %d using %d qubits", n, factor, other, num_qubits)
    return {
        "success": True,
        "n": n,
        "factors": (min(factor, other), max(factor, other)),
        "num_qubits": num_qubits,
    }


def is_prime(n):
    logger.debug("is_prime called with n=%d", n)
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
