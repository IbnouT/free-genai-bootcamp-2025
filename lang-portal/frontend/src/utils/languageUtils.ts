export function getFlagEmoji(countryCode: string): string {
    // Convert language code to country code for emoji
    const countryMapping: Record<string, string> = {
        'ja': 'jp', // Japanese -> Japan
        'fr': 'fr', // French -> France
        'ar': 'sa', // Arabic -> Saudi Arabia
        'es': 'es', // Spanish -> Spain
        'de': 'de', // German -> Germany
    }

    const code = countryMapping[countryCode.toLowerCase()] || countryCode
    const codePoints = code
        .toUpperCase()
        .split('')
        .map(char => 127397 + char.charCodeAt(0));
    
    return String.fromCodePoint(...codePoints);
} 