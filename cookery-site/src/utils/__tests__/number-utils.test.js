import { expect, test, describe } from 'vitest'
import { parseCommonFraction, formatCommonFraction } from '../number-utils'

describe('Parse plain numbers', () => {
    test('int is int', () => expect(parseCommonFraction('12')).toBe(12))
    test('float is float', () => expect(parseCommonFraction('4.7')).toBe(4.7))
})

describe('Parse fractional inputs', () => {
    test("1/10", () => expect(parseCommonFraction('1/10')).toBe(0.1))
    test("3/4", () => expect(parseCommonFraction('3/4')).toBe(3/4))
    test("1/3", () => expect(parseCommonFraction('1/3')).toBe(1/3))
})

describe('Format common fractions', () => {
    test("0.5 => 1/2", () => expect(formatCommonFraction(0.5)).toBe("1/2"))

    test("1/3 => 1/3", () => expect(formatCommonFraction(1/3)).toBe("1/3"))
    test("0.333 => 1/3", () => expect(formatCommonFraction(0.333)).toBe("1/3"))
    test("2/3 => 2/3", () => expect(formatCommonFraction(2/3)).toBe("2/3"))

    test("1/4 => 1/4", () => expect(formatCommonFraction(1/4)).toBe("1/4"))
    test("3/4 => 3/4", () => expect(formatCommonFraction(3/4)).toBe("3/4"))

    test("5/8 => 5/8", () => expect(formatCommonFraction(5/8)).toBe("5/8"))

    test("0.1 => 1/10", () => expect(formatCommonFraction(0.1)).toBe("1/10"))
})

describe('Invalid inputs', () => {
    test("empty", () => expect(parseCommonFraction('')).toBe(NaN))
    test("1//10", () => expect(parseCommonFraction('1//10')).toBe(NaN))
    test("12/b", () => expect(parseCommonFraction('12/b')).toBe(NaN))
    test("4/0", () => expect(parseCommonFraction('4/0')).toBe(NaN))
    test("12/1.5", () => expect(parseCommonFraction('4/0')).toBe(NaN))
    test("0.4/33", () => expect(parseCommonFraction('4/0')).toBe(NaN))
})