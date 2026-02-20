import { create } from 'zustand';
import { FILM_PRESETS } from '../utils/constants';

export const useFilmStore = create((set) => ({
  currentFilm: FILM_PRESETS[0],
  films: FILM_PRESETS,
  
  setCurrentFilm: (film) => set({ currentFilm: film }),
  
  addFilm: (film) => set((state) => ({ 
    films: [...state.films, film],
    currentFilm: film 
  })),
  
  updateFilm: (filmTitle, updates) => set((state) => ({
    films: state.films.map(f => 
      f.title === filmTitle ? { ...f, ...updates } : f
    ),
    currentFilm: state.currentFilm.title === filmTitle 
      ? { ...state.currentFilm, ...updates } 
      : state.currentFilm
  })),
}));
