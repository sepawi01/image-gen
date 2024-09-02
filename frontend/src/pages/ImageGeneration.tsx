// import {useEffect} from "react";
import ImageGallery from "../components/ImageGallery.tsx";
import PromptSelections from "../components/PromptSelections.tsx";
import PromptInput from "../components/PromptInput.tsx";
import {CircleLoader} from "react-spinners";
import {useAppContext} from "../contexts/AppContext.tsx";

export default function ImageGenerationPage() {

    const {generatingImages} = useAppContext()

    // Let's wait with fetching historical images until later
    // useEffect(() => {
    //
    //     fetch(import.meta.env.VITE_API_BASE_URL + '/api/images/user/123')
    //         .then(response => response.json())
    //         .then(data => {
    //             setUserImagesList(data);
    //         });
    // }, []);


    return (
        <div
            className="m-5 divide-y divide-gray-200 overflow-hidden rounded-lg bg-white shadow border-2 border-gray-200">
            <div className="px-4 py-5 sm:px-6">
                <div className="p-5">
                    <PromptSelections/>
                    <PromptInput/>
                </div>

            </div>
            <div className="px-4 py-5 sm:p-6">

                <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                    {generatingImages ? (
                        <div className="flex justify-center">
                            <CircleLoader color="#4F46E5"/>
                        </div>
                    ) : (
                        <ImageGallery />
                    )}
                </div>


            </div>
        </div>
    )
}