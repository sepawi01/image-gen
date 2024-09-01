import { ArrowDownOnSquareIcon, ArrowPathIcon, ClipboardDocumentListIcon, TrashIcon } from '@heroicons/react/24/outline'
import { Tooltip } from 'react-tooltip'
import { type UserImageData } from "../types/appTypes.ts";

type ImageGalleryProps = {
  userImages: UserImageData[];
}

export default function ImageGallery({ userImages } : ImageGalleryProps) {
  return (
    <ul role="list" className="grid grid-cols-2 gap-x-4 gap-y-8 sm:grid-cols-3 sm:gap-x-6 lg:grid-cols-4 xl:gap-x-8">
      {userImages.map((imageData) => (
        <li key={imageData.id} className="relative">
          <div className="group aspect-h-7 aspect-w-10 block w-full overflow-hidden rounded-lg bg-gray-100 focus-within:ring-2 focus-within:ring-indigo-500 focus-within:ring-offset-2 focus-within:ring-offset-gray-100 p-2">
              <img alt="" src={imageData.imageUrl} className="pointer-events-none object-cover group-hover:opacity-75" />
          </div>
          <div className="mt-3 px-3 flex justify-between">
            <button className="flex items-center justify-center w-8 h-8 border rounded-md hover:bg-gray-300 focus:outline-none">
              <ArrowDownOnSquareIcon className="w-5 h-5 text-gray-600" aria-hidden="true" data-tooltip-id="download-tooltip" data-tooltip-content="Ladda ner"/>
            </button>
            <Tooltip id="download-tooltip" />
            <button className="flex items-center justify-center w-8 h-8 border rounded-md hover:bg-gray-300 focus:outline-none">
              <ArrowPathIcon className="w-5 h-5 text-gray-600" aria-hidden="true" data-tooltip-id="regenerate-tooltip" data-tooltip-content="Ny variant"/>
            </button>
            <Tooltip id="regenerate-tooltip" />
            <button className="flex items-center justify-center w-8 h-8 border rounded-md hover:bg-gray-300 focus:outline-none">
              <ClipboardDocumentListIcon className="w-5 h-5 text-gray-600" aria-hidden="true" data-tooltip-id="copyprompt-tooltip" data-tooltip-content="Kopiera prompt" />
            </button>
            <Tooltip id="copyprompt-tooltip" />
            <button
                className="flex items-center justify-center w-8 h-8 border rounded-md hover:bg-gray-300 focus:outline-none">
              <TrashIcon className="w-5 h-5 text-gray-600" aria-hidden="true" data-tooltip-id="delete-tooltip" data-tooltip-content="Ta bort"/>
            </button>
            <Tooltip id="delete-tooltip" />
          </div>
        </li>
      ))}
    </ul>
  );
}