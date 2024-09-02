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
    const {prompt, setPrompt, n_images, quality, size, style, setUserImagesList, setGeneratingImages} = useAppContext();

    //TODO: Vi ska nog inte hämta bilderna från egen blob storage direkt. Antingen så visar vi dem
    // från de url:er som vi får från API:et eller så sparar vi dem i vår egen blob storage och hämtar alla bilder därifrån.
    // Jag behöver fixa hanteringen av hur bilderna visas i ImageGallery.tsx.
    const getSASToken = async (blobName: string) => {
        const apiUrl = `${getApiBaseUrl()}/api/images/blob/${blobName}`;

        try {
            const response = await fetch(apiUrl, {
                method: 'GET',
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            return data['imageUrl'];
        } catch (error) {
            console.error('Error fetching SAS token data:', error);
            return null;
        }
    };

    const handleGenerateClick = async () => {
        const userId = '123'; // Hardcoded until we have user authentication
        const queryParams = new URLSearchParams({
            prompt,
            n_images: n_images.toString(),
            quality,
            size,
            style,
        });

        const apiUrl = `${getApiBaseUrl()}/api/images/generate?user_id=${userId}&${queryParams.toString()}`;
        setGeneratingImages(true);

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            console.log('Generated data:', data);

            // Fetch SAS tokens for each image and update the imageUrl
            const updatedData = await Promise.all(
                data.map(async (d: any) => {
                    const imageUrl = await getSASToken(d.blobName);
                    return { ...d, imageUrl };
                })
            );

            // Update the user images list with the new data
            setUserImagesList((prevData) => [...prevData, ...updatedData]);
        } catch (error) {
            console.error('Error fetching generated data:', error);
        } finally {
            console.log("Done fetching generated data");
            setGeneratingImages(false);
        }
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