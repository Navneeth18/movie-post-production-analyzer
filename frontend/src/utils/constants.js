export const FILM_PRESETS = [
  { 
    title: "Echoes of Silence", 
    genre: "Drama", 
    budget: "₹2.5Cr", 
    budgetValue: 2.5,
    lang: "Hindi", 
    themes: "Family, Memory, Loss", 
    region: "Pan-India",
    director: "Unknown"
  },
  { 
    title: "The Urban Grind", 
    genre: "Thriller", 
    budget: "₹8Cr", 
    budgetValue: 8.0,
    lang: "Hindi/English", 
    themes: "Crime, Politics, Ambition", 
    region: "Metro Cities",
    director: "Unknown"
  },
  { 
    title: "Sundarbans", 
    genre: "Nature Drama", 
    budget: "₹1.2Cr", 
    budgetValue: 1.2,
    lang: "Bengali", 
    themes: "Environment, Survival", 
    region: "Eastern India + Intl",
    director: "Unknown"
  },
];

export const AUDIENCE_DATA = {
  "Drama": {
    segments: [
      { name: "Emotionally Engaged Adults", age: "28–45", size: 42, interest: ["Family stories", "Human drama", "Regional cinema"], platforms: ["Netflix", "Prime", "Mubi"] },
      { name: "Festival Circuit Watchers", age: "22–38", size: 28, interest: ["Award films", "Arthouse", "Documentaries"], platforms: ["MUBI", "SonyLIV", "Festivals"] },
      { name: "Regional Pride Audience", age: "35–60", size: 30, interest: ["Language cinema", "Cultural themes", "Local stars"], platforms: ["ZEE5", "Aha", "Theatres"] },
    ],
    traits: ["High emotional investment", "Word-of-mouth driven", "Festival circuit aware", "Streaming-first behavior"],
    dna: [82, 45, 67, 90, 38, 72]
  },
  "Thriller": {
    segments: [
      { name: "Urban Thrill Seekers", age: "18–32", size: 45, interest: ["Crime dramas", "Action", "Suspense"], platforms: ["Netflix", "Prime", "PVR"] },
      { name: "Binge Watchers", age: "22–35", size: 35, interest: ["Series format", "Cliffhangers", "Dark stories"], platforms: ["Netflix", "Hotstar", "Prime"] },
      { name: "Multiplex Crowd", age: "25–45", size: 20, interest: ["Big screen experience", "Weekend outings"], platforms: ["PVR", "INOX", "Cinepolis"] },
    ],
    traits: ["Social media savvy", "Trailer-driven decisions", "Influencer receptive", "Weekend release preference"],
    dna: [55, 88, 45, 62, 79, 85]
  },
};

export const PLATFORM_SCORES = {
  "Drama": [
    { name: "Netflix India", score: 87, deal: "₹2.8–4.2Cr", window: "6–8 months post-theatrical" },
    { name: "Amazon Prime", score: 74, deal: "₹1.8–3.0Cr", window: "8–12 months post-theatrical" },
    { name: "MUBI", score: 91, deal: "₹0.4–0.8Cr", window: "Simultaneous or day-and-date" },
    { name: "SonyLIV", score: 68, deal: "₹1.2–2.0Cr", window: "4–6 months post-theatrical" },
    { name: "ZEE5", score: 62, deal: "₹1.0–1.6Cr", window: "3–6 months" },
  ],
  "Thriller": [
    { name: "Netflix India", score: 92, deal: "₹4.5–8.0Cr", window: "4–6 months post-theatrical" },
    { name: "Amazon Prime", score: 88, deal: "₹3.5–6.0Cr", window: "6–8 months" },
    { name: "Hotstar", score: 75, deal: "₹2.0–3.5Cr", window: "6–10 months" },
    { name: "SonyLIV", score: 65, deal: "₹1.5–2.5Cr", window: "4–8 months" },
    { name: "JioCinema", score: 58, deal: "₹1.0–2.0Cr", window: "3–5 months" },
  ],
};

export const FESTIVALS = [
  { name: "MAMI Mumbai", deadline: "Jul 15", match: 94, category: "Indian Panorama", fee: "₹2,000", status: "Open" },
  { name: "BIFF Bengaluru", deadline: "Aug 1", match: 89, category: "Competition", fee: "₹1,500", status: "Open" },
  { name: "Sundance", deadline: "Sep 15", match: 72, category: "World Drama", fee: "$60", status: "Upcoming" },
  { name: "Berlin Berlinale", deadline: "Oct 30", match: 68, category: "Forum", fee: "€80", status: "Upcoming" },
  { name: "IFFI Goa", deadline: "Sep 1", match: 88, category: "Indian Panorama", fee: "₹0", status: "Open" },
  { name: "Busan BIFF", deadline: "Jul 31", match: 61, category: "New Currents", fee: "$40", status: "Open" },
];

export const COMP_FILMS = [
  { title: "Paanch Rupaiya", genre: "Drama", year: 2023, budget: "₹2Cr", collection: "₹18Cr", roi: "9x", strategy: "Festival → OTT", keywords: ["Family", "Rural"] },
  { title: "Vaanam Kottattum", genre: "Drama", year: 2020, budget: "₹3Cr", collection: "₹6Cr", roi: "2x", strategy: "Theatrical + OTT", keywords: ["Memory", "Urban"] },
  { title: "Jalsa (2022)", genre: "Drama Thriller", year: 2022, budget: "₹40Cr", collection: "₹200Cr+", roi: "5x", strategy: "Direct OTT (Prime)", keywords: ["Moral dilemma", "Urban"] },
  { title: "Pagglait", genre: "Drama Comedy", year: 2021, budget: "₹8Cr", collection: "₹60Cr OTT", roi: "7.5x", strategy: "Direct OTT → Theatrical", keywords: ["Family", "Identity"] },
];
