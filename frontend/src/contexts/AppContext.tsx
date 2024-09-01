import { ReactNode, createContext, useContext, useState, Dispatch, SetStateAction  } from "react";
import {type UserImageData } from "../types/appTypes.ts";

type AppContextType = {
  n_images: number;
  setNImages: Dispatch<SetStateAction<number>>;
  quality: string;
  setQuality: Dispatch<SetStateAction<string>>;
  size: string;
  setSize: Dispatch<SetStateAction<string>>;
  style: string;
  setStyle: Dispatch<SetStateAction<string>>;
  prompt: string;
  setPrompt: Dispatch<SetStateAction<string>>;
  userImagesList: UserImageData[];
  setUserImagesList: Dispatch<SetStateAction<UserImageData[]>>;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

type PromptProviderProps = {
    children: ReactNode;
}

export function AppProvider({ children } : PromptProviderProps)  {
    const [n_images, setNImages] = useState<number>(1);
    const [quality, setQuality] = useState<string>("standard");
    const [size, setSize] = useState<string>("1024x1024");
    const [style, setStyle] = useState<string>("natural");
    const [prompt, setPrompt] = useState<string>("");
    const [userImagesList, setUserImagesList] = useState<UserImageData[]>([]);

    const value: AppContextType = {
    n_images,
    setNImages,
    quality,
    setQuality,
    size,
    setSize,
    style,
    setStyle,
    prompt,
    setPrompt,
    userImagesList,
    setUserImagesList,
    };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>
}

export function useAppContext() {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('usePrompt has to be used inside a PromptProvider');
  }
  return context;
}