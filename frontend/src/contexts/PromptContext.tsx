import { ReactNode, createContext, useContext, useState, Dispatch, SetStateAction  } from "react";

type PromptContextType = {
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
}

type PromptProviderProps = {
    children: ReactNode;
}

const promptContext = createContext<PromptContextType>({
    n_images: 1,
    setNImages: () => {},
    quality: "standard",
    setQuality: () => {},
    size: "1024x1024",
    setSize: () => {},
    style: "natural",
    setStyle: () => {},
    prompt: "",
    setPrompt: () => {},
});

export function PromptProvider({ children } : PromptProviderProps)  {
    const [n_images, setNImages] = useState<number>(1);
    const [quality, setQuality] = useState<string>("standard");
    const [size, setSize] = useState<string>("1024x1024");
    const [style, setStyle] = useState<string>("natural");
    const [prompt, setPrompt] = useState<string>("");

    const value: PromptContextType = {
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
    };

  return <promptContext.Provider value={value}>{children}</promptContext.Provider>
}

export function usePrompt() {
  const context = useContext(promptContext);
  if (context === undefined) {
    throw new Error('usePrompt has to be used inside a PromptProvider');
  }
  return context;
}