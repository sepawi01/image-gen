import { useAppContext } from "../contexts/AppContext.tsx";

const getApiBaseUrl = (): string => {
    const backendBaseURL = import.meta.env.VITE_API_BASE_URL;

    if (backendBaseURL && backendBaseURL.trim() !== '') {
        return backendBaseURL;
    } else {
        const errorMessage = 'API_BASE_URL is not set or is empty';
        console.error(errorMessage);
        throw new Error(errorMessage);
    }
};

export default function PromptInput() {
    const {prompt, setPrompt, n_images, quality, size, style, setUserImagesArray} = useAppContext();

    const handleGenerateClick = async () => {

        const queryParams = new URLSearchParams({
            prompt,
            n_images: n_images.toString(),
            quality,
            size,
            style,
        });

        const apiUrl = `${getApiBaseUrl()}/api/images/generate?${queryParams.toString()}`;
        fetch(apiUrl, {
            method: 'POST',
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                setUserImagesArray(prevData => ({userImages: [...prevData.userImages, ...data]}));
            })
            .catch(error => {
                console.error('Error fetching generated data:', error);
            });
    };


    return <div className="flex space-x-4">
        <div className="flex-grow">
            <label htmlFor="prompt" className="block text-sm font-medium leading-6 text-gray-900">
                Prompt
            </label>
            <input
                type="text"
                id="prompt"
                name="prompt"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                className="mt-2 block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6"
            />
        </div>
        <div className="flex items-end">
            <button
                onClick={handleGenerateClick}
                className="mt-2 bg-indigo-600 text-white font-medium py-1.5 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:ring-offset-2">
                Generera
            </button>
        </div>
    </div>;
}