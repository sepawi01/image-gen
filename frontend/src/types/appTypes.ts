

export type UserImageData = {
    id: string;
    userId: string;
    timestamp: string;
    prompt: string;
    revisedPrompt: string;
    imageUrl: string;
    settings: {
        quality: string;
        size: string;
        style: string;
    }
}
