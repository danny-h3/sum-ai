'use client'

import { IconArrowRight, IconPlus } from '@tabler/icons-react';
import { ActionIcon, Paper, Textarea, useMantineTheme } from '@mantine/core';
import { MenuDropDown } from './menu-with-dropdown';
import { Dropzone, FileWithPath } from '@mantine/dropzone';
import { useState } from 'react';
import { FilePreviewCard } from './file-preview-card';
import { PostUpload } from '../lib/api';

export function InputWithButton() {
  const theme = useMantineTheme();

  const [fileArray, setFileArray] = useState<FileWithPath[]>([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleInputFieldChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputText(e.currentTarget.value)
  }

  const handleSubmit = async () => {
    if (isLoading) return; 

    if (!inputText && fileArray.length === 0) {
      return 
    }

    setIsLoading(true); 
    try { 
      const postStatus = await PostUpload(inputText, fileArray)

      if (postStatus === 200 ) {
        console.log("Success")
      }
      setInputText("")
      setFileArray([])
    } catch (err) {
      console.error("Internal error: ", err)
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey && !e.nativeEvent.isComposing) {
      e.preventDefault()
      handleSubmit()
    }
  } 

  return (
    <Dropzone 
      onDrop={(newFiles) => setFileArray( (previousArray) => [...previousArray, ...newFiles])} 
      activateOnClick={false}
      activateOnKeyboard={false}
    >
      <Paper
        radius="lg"
        withBorder
        p="md"
        >
          <ul className="flex flex-wrap gap-2">
            { fileArray.map((file, index) => (
              <li key={index}>
                <FilePreviewCard 
                  file={file} 
                  onRemove={() => setFileArray(prev => prev.filter((_, i) => i !== index))} />
              </li>
            ))}
          </ul>
        <Textarea
          size="md"
          variant="unstyled"
          autosize
          minRows={1}
          maxRows={8}
          placeholder="Summarize something ... "
          classNames={{ wrapper: 'w-full'}}
          value={inputText}
          onChange={handleInputFieldChange}
          onKeyDown={handleKeyDown}
        />
        
        <div className="flex justify-between w-full">
          <MenuDropDown 
            button={
              <ActionIcon
                size={32}
                radius="xl"
                variant="transparent"
                aria-label="Upload">
                  <IconPlus size={18} stroke={1.5}></IconPlus>
              </ActionIcon>
            }
            onFileSelect={(files) => setFileArray(prev => [...prev, ...files])}
          >
          </MenuDropDown>

          <ActionIcon
            size={32}
            radius="xl"
            color={theme.primaryColor}
            variant="filled"
            aria-label="Enter"
            loading={isLoading}
            onClick={handleSubmit}
          >
            <IconArrowRight size={18} stroke={1.5} />
          </ActionIcon>
        </div>

      </Paper>
    </Dropzone>
  );
}